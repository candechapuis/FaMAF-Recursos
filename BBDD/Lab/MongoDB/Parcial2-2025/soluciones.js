use('sample_airbnb');

// Ej. 1

db.listingsAndReviews.aggregate([
    {
        $match: {
            "review_scores.review_scores_rating": {$exists: true}
        }
    },
    {
        $group: {
            _id: "$address.country",
            prom_rating: {$avg: "$review_scores.review_scores_rating"},
            amount_of_raitings: {$count: {}}
        }
    },{
        $sort: {
            prom_rating:-1
        }
    }
]);


//Ej. 2

db.listingsAndReviews.aggregate([
    {
        $match: {
            last_review: {$exists: true}
        }
    },
    {
        $project: {
            _id: 1,
            name: 1,
            last_review: 1,
            amount_of_reviews: {$size: "$reviews"}
        }
    },{
        $sort: {
            last_review: -1
        }
    },{
        $limit: 20
    }

]);

//Ej. 3

db.createView(
    "top10_most_common_amenities",
    "listingsAndReviews",
    [
        {
            $unwind: "$amenities"
        },{
            $group: {
                _id: {amenitie: "$amenities"},
                count: {$count: {}}
            }
        },{
            $sort: {
                count: -1
            }
        },{
            $limit: 10
        }
    ]
);


//Ej. 4

db.listingsAndReviews.updateMany(
    {
        "address.country": "Brazil",
        "review_scores.review_scores_rating": {$exists: true} 
    },
    [
      {
            $addFields: {
                quality_label: {
                    $switch: {
                        branches: [
                            {case: {$gte: ["$review_scores.review_scores_rating", 90]}, then: "High"},
                            {case: {$gte: ["$review_scores.review_scores_rating", 70]}, then: "Medium"},
                        ],
                        default: "Low"
                    }
                }
            }
        }
    ]
);

//Ej. 5

db.runCommand({
    collMod: "listingsAndReviews",
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: [
                "_id",
                "name",
                "amenities",
                "address",
                "review_scores",
                "reviews"
            ],
            properties: {
                _id: {
                    bsonType: "string"
                },
                name: {
                    bsonType: "string",
                },
                amenities: {
                    bsonType: "array",
                    minItems: 1,
                    items: {
                        bsonType: "string"
                    }
                },
                address: {
                    bsonType: "object",
                    required: ["street","country"],
                    properties: {
                        street: {
                            bsonType: "string"
                        },
                        country: {
                            bsonType: "string"
                        }
                    }
                },
                review_scores: {
                    bsonType: "object",
                    // las propiedades no van en required
                    //porque puede haber airbnbs sin reviews
                    properties: {
                        review_scores_accuracy: {
                            bsonType: "int",
                            minimum: 0,
                            maximum: 10
                        },
                        review_scores_cleanliness: {
                            bsonType: "int",
                            minimum: 0,
                            maximum: 100
                        },
                        review_scores_checkin: {
                            bsonType: "int",
                            minimum: 0,
                            maximum: 10
                        },
                        review_scores_communication: {
                            bsonType: "int",
                            minimum: 0,
                            maximum: 10
                        },
                        review_scores_location: {
                            bsonType: "int",
                            minimum: 0,
                            maximum: 10
                        },
                        review_scores_value: {
                            bsonType: "int",
                            minimum: 0,
                            maximum: 10
                        },
                        review_scores_rating: {
                            bsonType: "int",
                            minimum: 0,
                            maximum: 100
                        }
                   }
                },
                reviews: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: [
                            "listing_id",
                            "reviewer_id",
                            "reviewer_name",
                        ],
                        properties: {
                            listing_id: {
                                bsonType: "string"
                            },
                            reviewer_id: {
                                bsonType: "string"
                            },
                            reviewer_name: {
                                bsonType: "string"
                            },
                            comments: {
                                bsonType: "string"
                            }
                        }
                    }
                }

            }
        }
    }
});

// caso de éxito
db.listingsAndReviews.insertOne(
    {
        _id: "78965489",
        name: "cabañoski", 
        address: {
            street: "calle123",
            country: "Argentina"
        },
        amenities: ["Wifi", "Essentials"],
        review_scores: {
            review_scores_accuracy: 9,
            review_scores_cleanliness: 9,
            review_scores_checkin: 10,
            review_scores_communication: 10,
            review_scores_location: 10,
            review_scores_value: 9,
            review_scores_rating: 89
        },
        reviews: [
            {
                listing_id:  "78965489",
                reviewer_id: "45673654",
                reviewer_name: "Cande",
                comments: "tope"
            }
        ]
    }
);

// casos de fallo

// 'review_scores_rating' es mayor que 100
db.listingsAndReviews.insertOne(
    {
        _id: "78965490",
        name: "cabañoski", 
        address: {
            street: "calle123",
            country: "Argentina"
        },
        amenities: ["Wifi", "Essentials"],
        review_scores: {
            review_scores_accuracy: 9,
            review_scores_cleanliness: 9,
            review_scores_checkin: 10,
            review_scores_communication: 10,
            review_scores_location: 10,
            review_scores_value: 9,
            review_scores_rating: 234
        },
        reviews: [
            {
                listing_id:  "78965490",
                reviewer_id: "45673654",
                reviewer_name: "Cande",
                comments: "tope"
            }
        ]
    }
);

// falta el campo 'street' en 'address'
db.listingsAndReviews.insertOne(
    {
        _id: "78965491",
        name: "cabañoski", 
        address: {
            country: "Argentina"
        },
        amenities: ["Wifi", "Essentials"],
        review_scores: {
            review_scores_accuracy: 9,
            review_scores_cleanliness: 9,
            review_scores_checkin: 10,
            review_scores_communication: 10,
            review_scores_location: 10,
            review_scores_value: 9,
            review_scores_rating: 89
        },
        reviews: [
            {
                listing_id:  "78965491",
                reviewer_id: "45673654",
                reviewer_name: "Cande",
                comments: "tope"
            }
        ]
    }
);