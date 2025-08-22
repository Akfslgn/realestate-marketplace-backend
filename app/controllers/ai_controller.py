from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from openai import OpenAI

from app.services.listing_service import ListingService

ai_bp = Blueprint("ai", __name__)


def get_ai_client():
    """Get OpenAI client"""
    return OpenAI()


AI_MODEL = "gpt-4.1-nano"


@ai_bp.route("/ai/chat/listing/<int:listing_id>", methods=["POST"])
@jwt_required()
def chat_about_listing(listing_id: int):
    """Chat about specific listing"""

    # capture the payload from request
    data = request.get_json()
    user_message = data.get("message", "").strip()

    # basic validation
    if not user_message:
        return jsonify({"error": "Message is required."}), 400

    if len(user_message) > 500:
        return jsonify({"error": "Message is too long, no more than 500 characters allowed"}), 400

    # prepare context for the model

    listing = ListingService.get_listings_by_id(listing_id)

    if not listing:
        return jsonify({"error": "Listing not found"}), 404

    # create the context with retrieved listing

    context = f"""
        You are a helpful real estate assistant. Here is the property details:
        Title: {listing.title}
        Price: ${listing.price:,.2f}
        Type: {listing.property_type}
        Bedrooms: {listing.bedrooms}
        Bathrooms: {listing.bathrooms}
        Area: {listing.area_sqft}
        Location: {listing.address}, {listing.city}, {listing.state}, {listing.zip_code}
        Description: {listing.description or 'No Description'}
        Answer questions about this property helpfully and briefly.
        Be persuasive on why to buy this property and provide facts about the listing.
        If there are any questions about inventory mention to navigate to the Listings page or use 
        AI Advanced Search to find the ideal property for user.
        If the user asks some web serach or research related questions, do a quick web search and provide real facts.
        Do not provide more than 100 words.
        """

    # call OpenAI
    client = get_ai_client()
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.7,
        max_tokens=300
    )

    return jsonify({
        "message": response.choices[0].message.content,
        "listing_id": listing_id
    })


@ai_bp.route("/ai/search", methods=["POST"])
@jwt_required()
def search_listings():

    data = request.get_json()
    search_query = data.get("query", "").strip()

    if not search_query:
        return jsonify({"error": "Query is required."}), 400

    if len(search_query) > 300:
        return jsonify({"error": "Query is too long, no more than 300 characters allowed"}), 400

    listings = ListingService.get_all_listings()

    if not listings:
        return jsonify({"error": "No listings available"}), 404

    context = "You are a real estate assistant. Here are the available properties: \n\n"

    for listing in listings:
        context += f"""
            Property ID: {listing.id}
            Title: {listing.title}
            Price: ${listing.price:,.2f}
            Type: {listing.property_type}
            Bedrooms: {listing.bedrooms}
            Bathrooms: {listing.bathrooms}
            Area: {listing.area_sqft}
            Location: {listing.address}, {listing.city}, {listing.state}, {listing.zip_code}
            Description: {listing.description or 'No Description'}
        --------------------------------------
        """

    context += f"""
        Based on this request: {search_query}
        Recommend suitable properties and respond with:
        1. A helpful message explaining the recommendation.
        2. List of Property IDs of recommended properties as numbers only.
        Format: Respond with JSON like:
        {{"message": "Your helpful message here", "property_ids": [1,2,3]}}
    """

    client = get_ai_client()

    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": search_query}
        ],
        temperature=0.7,
        max_tokens=400
    )

    try:
        import json
        ai_response = json.loads(response.choices[0].message.content)
        message = ai_response.get("message", "")
        property_ids = ai_response.get("property_ids", [])
    except:
        message = response.choices[0].message.content
        property_ids = []

    recommeded_listings = []

    for p_id in property_ids:
        listing = ListingService.get_listings_by_id(p_id)
        if listing:
            recommeded_listings.append(listing.serialize())

    return jsonify({
        "message": message,
        "recommended_listings": recommeded_listings
    })
