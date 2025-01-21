(define (domain meal-planning)
    (:requirements :strips :typing)

    (:types
        robot
        human
        recipe
    )

    (:predicates
        (recipe-suggested)
        (recipe-selected ?r - recipe)
        (expired-ingredients-identified)
        (food-fresh ?r - recipe)
    )

    (:action suggest-recipe
        :parameters (?rob - robot ?rec - recipe)
        :effect (recipe-suggested)
    )

    (:action select-recipe
        :parameters (?h - human ?rec - recipe)
        :precondition (recipe-suggested)
        :effect (recipe-selected ?rec)
    )

    (:action expiration-date-query
        :parameters (?rob - robot ?rec - recipe)
        :precondition (and
                (recipe-selected ?rec)

            )
        :effect (expired-ingredients-identified)
    )

    (:action resolve-expired-ingredients
        :parameters (?h - human ?rec - recipe)
        :precondition (expired-ingredients-identified)
        :effect (food-fresh ?rec)
    )

)