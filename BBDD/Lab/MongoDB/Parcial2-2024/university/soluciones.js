use('university');

//Ej. 1

db.grades.find(
    {
        scores: {
            $elemMatch: {
                $or: [
                    {type: "exam",
                    score: {$gte: 80}},
                    {type: "quiz",
                    score: {$gte: 90}},
                ]
            },
            $not: {
                $elemMatch: {
                    type: "homework",
                    score: {$lt: 60}
                }
            }
        }
    },
    {
        _id: 0
    }
).sort(
    {class_id: -1, student_id: 1}
);
/* RECORDAR $ELEMMATCH PARA CORROBORAR CONDICIONES SOBRE
ELEMENTOS DE ARREGLOS*/

//Ej. 2

db.grades.aggregate([
    {
        $match: {
            $or: [
                {class_id: 20},
                {class_id: 220},
                {class_id: 420}
            ]
        }
    },{
        $group: {
            _id: {student:"$student_id"},
            scores_p_class: {
                $addToSet: {
                    class_id: "$class_id",
                    maxScore: {$max: "$scores.score"},
                    minScore: {$min: "$scores.score"},
                    avgScore: {$avg: "$scores.score"}
                }

            }
            
        }
    },{
        $sort:{
            student_id: 1,
            "scores_p_class.class_id": 1
        }
    }
]);

//Ej. 3

db.grades.aggregate([
    {
        $project: {
            class_id: 1,
            exam_scores: {
                $filter: {
                    input: "$scores",
                    as: "scores",
                    cond: {$eq: ["$$scores.type", "exam"]}
                }
            },
            quiz_scores: {
                $filter: {
                    input: "$scores",
                    as: "scores",
                    cond: {$eq: ["$$scores.type", "quiz"]}
                }
            }
        }
    },{
        $group: {
            _id: "$class_id",
            maxExScore: {$max: "$exam_scores.score"},
            maxQuScore: {$max: "$quiz_scores.score"},
        }
    },{
        $sort: {
            _id: 1
        }
    }
]);

//Ej.4

db.createView(
    "top10Students",
    "grades",
    [    
        {
            $project: {
                student_id: 1,
                class_id: 1,
                class_promedy: {
                    $avg: "$scores.score"
                }
            }
        },{
            $group: {
                _id: "$student_id",
                allTimePromedy: {$avg: "$class_promedy"}
            }
        },{
            $sort: {
                allTimePromedy: -1
            }
        },{
            $limit: 10
       }

    ]
);


// db.grades.aggregate([
//     {
//         $project: {
//             student_id: 1,
//             class_id: 1,
//             class_promedy: {
//                 $avg: "$scores.score"
//             }
//         }
//     },{
//         $group: {
//             _id: "$student_id",
//             allTimePromedy: {$avg: "$class_promedy"}
//         }
//     },{
//         $sort: {
//             allTimePromedy: -1
//         }
//     },{
//         $limit: 10
//     }

// ]);

//Ej. 5

db.grades.updateMany(
    {class_id: 339},
    [
        {
            $addFields: {
                score_avg: {$avg: "$scores.score"},
            }
        },{
            $addFields: {
                letter: {
                    $switch: {
                        branches: [
                            {case: {$lt: ["$score_avg", 60]}, then: "NA"},
                            {case: {$lt: ["$score_avg", 80]}, then: "A"},
                            {case: {$lte: ["$score_avg", 100]}, then: "P"}
                        ]
                    }
                }
            }
        }
    ]
);

//Ej. 6

db.runCommand({
    collMod: "grades",
    validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["student_id", "class_id", "scores"],
                properties: {
                    student_id: {
                        bsonType: "int"
                    },
                    class_id: {
                        bsonType: "int"
                    },
                    scores: {
                        bsonType: "array",
                        minItems: 4,
                        items: {
                            bsonType: "object",
                            required: ["type", "score"],
                            properties: {
                                type: {
                                    enum: ["exam", "quiz", "homework"]
                                },
                                score: {
                                    bsonType: "double"
                                }
                            }
                        }
                    }
                }
            }            
        }  
    }
);

// fail cases

// not all score.type are valid (pruebita is not a valid type)
db.grades.insertOne(
    {student_id: 44444, class_id: 444, 
        scores: [
            {type: "exam",
            score: 65.89},
            {type: "pruebita",
            score: 65.89},
            {type: "quiz",
            score: 65.89},
            {type: "homework",
            score: 65.89},

    ]}
);

// the scores array doesn't have at leats 4 elements
db.grades.insertOne(
    {student_id: 44444, class_id: 444, 
        scores: [
            {type: "exam",
            score: 65.89},
            {type: "homework",
            score: 65.89},
            {type: "quiz",
            score: 65.89},
    ]}
);

// succesfull case

db.grades.insertOne(
    {student_id: 44444, class_id: 444, 
        scores: [
            {type: "exam",
            score: 65.89},
            {type: "homework",
            score: 65.89},
            {type: "quiz",
            score: 65.89},
            {type: "homework",
            score: 65.89},

    ]}
);
