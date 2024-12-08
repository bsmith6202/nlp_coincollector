(define (problem exploration)
  (:domain environment)
  (:objects
    kitchen l1 - location
    north south east west - direction
  )
  (:init
    (at kitchen)
    (visited kitchen)
    (connected kitchen l1 east)
    (connected l1 kitchen west)
    (closed_door kitchen l1 east)
    (closed_door l1 kitchen west)
  )
  (:goal 
    (exists (?x - location)
        (and
            (not (visited ?x))
            (at ?x)
        )
    )
  )
)