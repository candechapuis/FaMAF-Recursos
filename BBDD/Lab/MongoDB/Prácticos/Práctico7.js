use ('mflix');
//Ej. 1
db.users.insertMany([
    { name: "Candelaria Chapuis",
        email: "cande@gmail.com",
        password: "pw"
    },
    { name: "Candelaria Canepa",
        email: "cande2@gmail.com",
        password: "pw"
    },
    { name: "Fiona Lacase",
        email: "fiokpop@gmail.com",
        password: "pw"
    },
    { name: "Juana Robredo",
        email: "juana@gmail.com",
        password: "pw"
    },
    { name: "ángeles Sueldo",
        email: "anyu@gmail.com",
        password: "pw"
    }
]);

const commentedMovie =  db.movies.findOne({title: "Titanic"});

db.comments.insertMany([
    { name: "Candelaria Chapuis",
        email: "cande@gmail.com",
        text: "Buenísima... Mejor que las más actuales.",
        movie_id: commentedMovie._id
    },
    { name: "Candelaria Canepa",
        email: "cande2@gmail.com",
        text: "Buenísima... Mejor que las más actuales.",
        movie_id: commentedMovie._id
    },
    { name: "Fiona Lacase",
        email: "fiokpop@gmail.com",
        text: "Buenísima... Mejor que las más actuales.",
        movie_id: commentedMovie._id
    },
    { name: "Juana Robredo",
        email: "juana@gmail.com",
        text: "Buenísima... Mejor que las más actuales.",
        movie_id: commentedMovie._id
    },
    { name: "ángeles Sueldo",
        email: "anyu@gmail.com",
        text: "Buenísima... Mejor que las más actuales.",
        movie_id: commentedMovie._id
    }
]);

// Ej. 2
db.movies.find({year: {$gte: 1990, $lte: 1999}, "imdb.rating": {$type: "double"}},{title: 1, year: 1, 
    cast:1, directors:1, "imdb.rating": 1}
    ).sort({"imdb.rating": -1}
    ).limit(10);

    // highest rating: 9.4

// Ej. 3

// this returns the comments
db.comments.aggregate([
    {
        $match: {
            movie_id: ObjectId("573a1399f29313caabcee886"),
            date: {
                $gte: new Date ('2014-01-01'),
                $lte: new Date ('2016-12-31')
            }
        }
    },
    {$project: {name:1,email:1,text:1,date:1}},
    {$sort: {date:1}}
]);

//this returns the number of comments with those caraceristics

db.comments.aggregate([
    {
        $match: {
            movie_id: ObjectId("573a1399f29313caabcee886"),
            date: {
                $gte: new Date ('2014-01-01'),
                $lte: new Date ('2016-12-31')
            }
        }
    },
    {$project: {_id: 0, movie_id: 0}},
    {$sort: {date: 1}},
    {$count: "Amount Of Comments"}
]);


//Ej. 4

db.comments.find(
    {email: "patricia_good@fakegmail.com"},
    {_id: 0, email:0}
).sort({date:-1}
).limit(3);

//Ej. 5

db.movies.aggregate([
    {
        $match: {
            genres: {$in: ["Drama", "Action"]},
            languages: {$size:1},
            $or: [ 
                {"imdb.votes": {$gte: 9},
                runtime: {$gte: 180}}]}
    },{
        $project: {
            title: 1,
            languages: 1,
            genres: 1,
            released: 1,
            "imdb.votes": 1}
    },{
        $sort: {
            released: 1,
            "imdb.votes": -1}
    }
]);

//Ej. 6

db.theaters.aggregate([
    {
        $match: {
            $or: [
                {"location.address.state": "CA"},
                {"location.address.state": "NY"},
                {"location.address.state": "TX"}
            ],
            "location.address.city": {
                $regex: /^F/
            }
        }
    },{
        $sort: {
            "location.address.state": 1,
            "location.address.city": 1
        }
    },{
        $project: {
            theaterId: 1,
            "location.address.state": 1,
            "location.address.city": 1,
            "location.geo.coordinates": 1
        }
    }
]);

//Ej. 7

db.comments.updateOne(
    {_id: ObjectId("5b72236520a3277c015b3b73")},
    {
        $set: {
            text: "mi mejor comentario",
            date: new Date()
        }
    }
);

//Ej.8

db.users.updateOne(
    {email: "joel.macdonel@fakegmail.com"},
    {
        $set: {
            password: "some password"
        }
    },
    {upsert: true}
);

// Ej. 9

db.users.deleteMany(
    {email: "victor_patel@fakegmail.com",
     date: {
        $gte: new Date('1980-01-01'),
        $lte: new Date('1980-12-31')
        },
    }
);

// Ej. 10
// from here, use restaurantdb
use('restaurantdb');

db.restaurants.aggregate([
    {
        $match: {
            "grades.date": {
                $gte: new Date('2014-01-01'),
                $lte: new Date('2015-12-31')},
            "grades.score" : {
                $gt: 70,
                $lte: 90}
        }
    }, {
        $project: {restaurant_id: 1, grades: 1}
    }
]);

db.restaurants.updateOne(
    {restaurant_id: "50018608"},
    {
        $addToSet: {
            grades: {
                $each: [{
                            "date" : ISODate("2019-10-10T00:00:00Z"),
                            "grade" : "A",
                            "score" : 18
                        },
                        {
                            "date" : ISODate("2020-02-25T00:00:00Z"),
                            "grade" : "A",
                            "score" : 21
                        }]
            }
        }
    }
);