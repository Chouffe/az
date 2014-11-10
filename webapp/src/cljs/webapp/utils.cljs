(ns webapp.utils)

(defn mean
  [xs]
  (if-not (seq xs)
    0
    (/ (reduce + xs) (count xs))))

(defn sqrt
  [x]
  (when (pos? x)
    (js/Math.sqrt x)))

(defn std
  [s]
  (let [m (mean s)]
    (sqrt
      (/ (reduce + (map #(* (- % m)
                            (- % m))
                        s))
         (count s)))))

(defn scale-for-bar-charts
  [data]
  (let [sum (reduce + (map second data))
        scale (fn [[label frequency]]
                [label (/ (* 100 frequency) sum)])]
    (map scale data)))

(defn parse-json
  ([s] (parse-json s true))
  ([s keywordize-keys?]
     (js->clj (js/JSON.parse s) :keywordize-keys keywordize-keys?)))

