(ns webapp.utils.stats)

(defn mean
  [xs]
  (if-not (seq xs)
    0.0
    (/ (float (reduce + xs)) (count xs))))

(defn sqrt
  [x]
  (when (pos? x)
    (Math/sqrt x)))

(defn std
  [s]
  (let [m (mean s)]
    (sqrt
      (/ (float (reduce + (map #(* (- % m)
                                   (- % m))
                               s)))
         (count s)))))

