(define-param rvecs (list (vector3 1 0 0) (vector3 0 1 0) (vector3 0 0 1)))
(define-param epsin 11.0)
(define-param epsout 1.0)
(define-param supercell 1)
(define-param r1 0.18)
(define-param nbands 12)
(define-param r2 0.18)
(define-param r_defect 0.76)
(define-param h (/ (sqrt 3) 2))
(define-param kvecs (list (vector3 0.0 0.0 0.0))) ; list of k-vectors (list of kvecs or string to kvecs data file)
(define-param Ws      '())    ; point group parts of symops; see SYMMETRY EIGENVALUES part
(define-param ws      '())
(define-param opidxs  '())

(include "aux-functionality.scm")
(include "print-symeigs.scm")

(define eps (make dielectric (epsilon epsin)))
(set! num-bands nbands)
(set! resolution 16)

(set! geometry-lattice (make lattice (size supercell supercell supercell)
            (basis1 (vector3 1 0 0)) (basis2 (vector3 0 1 0)) (basis3 (vector3 0 0 1))
            (basis-size 1 1 1)))

(define ax1 (vector3 1 1 1))
(define ax2 (vector3 -1 -1 1))
(define ax3 (vector3 1 -1 -1))
(define ax4 (vector3 -1 1 -1)) 

(define center1 (vector3 0.25 0.25 0.25))
(define center2 (vector3 -0.25 -0.25 0.25))
(define center3 (vector3 0.25 -0.25 -0.25))
(define center4 (vector3 -0.25 0.25 -0.25))


(define cylinder1 (make cylinder
                       (center center1) (radius r1) (height h) (axis ax1)
                       (material eps)))
(define cylinder2 (make cylinder
                       (center center2) (radius r2) (height h) (axis ax2)
                       (material eps)))
(define cylinder3 (make cylinder
                       (center center3) (radius r1) (height h) (axis ax3)
                       (material eps)))
(define cylinder4 (make cylinder
                       (center center4) (radius r2) (height h) (axis ax4)
                       (material eps)))

(set! geometry (list cylinder1 cylinder2 cylinder3 cylinder4) )
(set! geometry (geometric-objects-lattice-duplicates geometry))
(cond ((> supercell 1) (set! geometry (append geometry 
                      (list (make sphere (center 0 0 0) 
                                  (radius r_defect)
                                  (material eps)))))
))
; set kpoints
(set! k-points kvecs)
(init-params NO-PARITY true)

(cond ((not (null? Ws)) ; run only if some {W|w} operations were provided
    (do ((i 0 (+ i 1))) ((= i (length kvecs)))
        (let ( (opidxs-i (list-ref opidxs i)) )
            ; solve for eigenmodes at current k-point
            (solve-kpoint (list-ref kvecs i))

            ; loop over each {W|w} operation referenced by opidxs[i] at kvecs[i]
            (do ((j 0 (+ j 1))) ((= j (length opidxs-i)))
                (let* ( (idx (list-ref opidxs-i j))
                        (W   (list-ref Ws       (- idx 1)))
                        (w   (list-ref ws       (- idx 1))) )
                    ; compute & print {W|w}[opidxs[i][j]] sym-eigs at k[i]
                    (print-symeigs (+ i 1) W w (compute-symmetries W w))
                )
            )
        )
    )
))

(quit)
;(run)


