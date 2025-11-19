use ('mflix');

// Ej. 1

db.theaters.aggregate([
    {
        $group: {
            _id: "$location.address.state",
            theaterAmount: {$count: {}}
        }
    }
]);

//Ej. 2

db.theaters.aggregate([
    {
        $group: {
            _id: "$location.address.state",
            theaterAmount: {$count: {}}
        }
    },
    {
        $match: {
            theaterAmount: {$gte: 2}
        }
    },
    {
        $count: "statesWith2Or+Theaters"
    }
]);

//Ej. 3

    // without aggregation pipeline

db.movies.find(
    {
        directors: {$in: ["Louis Lumière"]}
    }
).count();

    // with aggregation pipelina

db.movies.aggregate([
    {
        $match: {
            directors: {$in: ["Louis Lumière"]}
        }
    },{
        $count: "MoviesDirectedByLouLumière"
    }
]);

//Ej. 4

// without aggregation pipeline

db.movies.find(
    {
        released: {
            $exists: true,
            $gte: new Date('1950-01-01'),
            $lte: new Date('1959-12-31')
        }         
    }
).count();

db.movies.aggregate([
    {
        $match: {
            released: {
                $exists: true,
                $gte: new Date('1950-01-01'),
                $lte: new Date('1959-12-31')
            }     
        }
    },{
        $count: "50sMovies"
    }
]);

//Ej. 5

db.movies.aggregate([
    {
        $unwind: "$genres"
    },{
        $group: {
            _id: "$genres",
            amount: {$count: {}}
        }
    },{
        $sort: {amount: -1}
    },{
        $limit: 10
    }
]);

//Ej. 6

db.comments.aggregate([
    {
        $group: {
            _id: {"email": "$email","name": "$name"},
            amount: {$count: {}}
        }
    },{
        $sort: {
            amount: -1
        }
    },{
        $limit: 10
    }
    
]);

//Ej. 7

db.movies.aggregate([
    {
        $group: {
            _id: "$year",
            avgRating: {$avg: "$imdb.rating"},
            minRating: {$min: "$imdb.rating" },
            maxRating: {$max: "$imdb.rating" },
            
        }
    },{
        $match: {
            _id: {
                $gte: 1980,
                $lte: 1989
            },
            $and: [
                {maxRating: {$type: "double"}},
                {minRating: {$type: "double"}}
            ]
        }
    },{
        $sort: {avgRating: -1}
    }
]);

//Ej. 8

// movies has a mflix_comments key .-.
db.comments.aggregate([
    {
        $lookup: {
            from: "movies",
            localField: "movie_id",
            foreignField: "_id",
            pipeline: [
                {
                    $project: {
                        _id: 0,
                        title: 1,
                        year: 1
                    }
                }
            ],
            as: "movie_descrip"
        }
    },{
        $group: {
            _id: "$movie_descrip",
            amountOfComments: {$count: {}}
        }
    }
]);

//Ej. 9

db.createView(
    "mostCommentedGenres",
    "movies",
    [
        {
            $unwind: "$genres"

        },{
            $group: {
                _id: "$genres",
                comments: {$sum: "$num_mflix_comments"}
            }
        },{
            $sort: {comments: -1}
        },{
            $limit: 5
        }
    ]
);

//Ej. 10

db.movies.aggregate([
    {
        $match: {
            directors: {$in: ["Jules Bass"]}
        }
    },{
        $unwind: "$cast"
    },{
        $group: {
            _id: {
                "actor/ress": "$cast", 
            },
            movies: {
                $addToSet: {
                    title: "$title", 
                    year: "$year"
                }
            }
        }
   },{
        $match: {
            "movies.2": {
                $exists: true
            }
        }
   }
]);

//Ej. 11

db.comments.aggregate([
    {
        $lookup: {
            from: "movies",
            let: {
                movie_id: "$movie_id", 
                cmntMonth: {$month: "$date"},
                cmntYear: {$year: "$date"}
            },
            pipeline: [
                {
                    $match: {
                        $expr: {
                            $and: [
                                {$eq: ["$_id", "$$movie_id" ]},
                                {$eq: [{$month: "$released"}, "$$cmntMonth"]},
                                {$eq: [{$year: "$released"}, "$$cmntYear"]}
                            ]
                        }
                    }
                },{
                    $project: {
                        title: 1,
                        released: 1
                    }
                }
            ],
            as: "commentedMovie"
        }
    },{
        $match: {
            commentedMovie: {$ne: []}
        }
    },{
        $group: {
            _id: {name: "$name", email: "$email"},
            "cmntDate+ReleasedDate": {
                $addToSet: {
                    movie: {$first: "$commentedMovie"},
                    cmntDate: "$date"
                }
            }
        }
    }
]);

//Ej. 12

use ('restaurantdb');

// using $group

db.restaurants.aggregate([
    {
        $unwind: "$grades"
    },{
        $group: {
            _id: {id: "$restaurant_id", name: "$name"},
            maxGrade:  {$max: "$grades.grade"},
            maxScore: {$max: "$grades.score"},
            minGrade:  {$min: "$grades.grade"},
            minScore: {$min: "$grades.score"},
            accumScore: {$sum: "$grades.score"}
        }
    }
]);

// using the grade array

db.restaurants.aggregate([
    {
        $addFields: {
            "maxScore": {$max: "$grades.score"},
            "minScore": {$min: "$grades.score"},
            "accumScore": {$sum: "$grades.score"}
        }
    },{
        $project: {
            _id:0, 
            restaurant_id:1,
            name: 1,
            maxScore: 1,
            minScore: 1,
            accumScore: 1,
        }
    }
]);

// using $reduce

db.restaurants.aggregate([
    {
        $addFields: {
            "maxScore": {$max: "$grades.score"},
            "minScore": {$min: "$grades.score"},
            "accumScore": {$reduce: {
                input: "$grades",
                initialValue: 0,
                in: {$sum: ["$$value", "$$this.score"]}
            }}
        }
    },{
        $project: {
            _id:0, 
            restaurant_id:1,
            name: 1,
            maxScore: 1,
            minScore: 1,
            accumScore: 1,
        }
    }
]);

// Ej. 13

db.restaurants.updateMany({},
    [
        {
        $addFields: { 
            average_score: {
                $avg: "$grades.score"
            }
        }
        },{
            $addFields: {
                grade: {
                    $switch: {
                        branches: [
                            { case: {$lt: ["$average_score", 14]}, then: "A" },
                            { case: {$lt: ["$average_score", 28]}, then: "B" },
                            { case: {$gte: ["$average_score", 28]}, then: "C" },
                        ]
                    }
                }

            }
        }
    ]
);
