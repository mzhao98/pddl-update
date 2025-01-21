(define (problem choose-meal)
    (:domain meal-planning)

    (:objects
        robot1 - robot
        human1 - human
        recipe1 - recipe
    )

    (:init
    )

    (:goal (and
        (recipe-selected recipe1)
        (food-fresh recipe1)
        )
    )
)