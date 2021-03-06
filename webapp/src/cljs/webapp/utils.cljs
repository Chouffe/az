(ns webapp.utils)

(defn mean
  [xs]
  (if-not (seq xs)
    0
    (/ (float (reduce + xs)) (count xs))))

(defn sqrt
  [x]
  (when (pos? x)
    (js/Math.sqrt x)))

(defn std
  [xs]
  (let [m (mean xs)]
    (sqrt
      (/ (float (reduce + (map #(* (- % m)
                            (- % m))
                        xs)))
         (count xs)))))

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


(defn prevent-default
  "Calls prevent-default on an event, then calls the input function with no
   arguments"
  [f]
  (fn [event] (.preventDefault event) (f)))
