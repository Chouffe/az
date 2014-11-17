(ns webapp.utils.data
  (:require [webapp.utils.stats :as statsu]))

(defn point->results-map
  [datapoints]
  (->> datapoints
       (group-by :features)
       (mapv (fn [[point xs]]
               [point {:result (mapv :result xs)
                       :time (mapv :time xs)}]))
       (mapv (fn [[point {:keys [result] :as m}]]
               [point (assoc m
                             :mu (statsu/mean result)
                             :sigma (or (statsu/std result) 0))]))
       (into {})))

(defn datapoints->convergence-data
  [datapoints features]
  (let [result-maps (point->results-map datapoints)
        point->result-sorted-by-time
        (sort-by (comp :time second)
                 (mapv (fn [[point {:keys [time] :as m}]]
                         (let [recent-time (last (sort time))]
                           [point
                            (select-keys
                              (assoc m :time recent-time)
                              [:time :mu])]))
                       result-maps))]
    (->> features
         (mapv
           (fn [[feature-name feature-map]]
             [feature-name
              (mapv (fn [[point _]]
                      (get point (keyword feature-name) 0))
                    point->result-sorted-by-time)]))
         (into {}))))

(defn datapoints->cost-function-data
  [datapoints]
  (let [result-maps (point->results-map datapoints)
        point->result-sorted-by-time
        (sort-by (comp :time second)
                 (mapv (fn [[point {:keys [time] :as m}]]
                         (let [recent-time (last (sort time))]
                           [point
                            (select-keys
                              (assoc m :time recent-time)
                              [:time :mu])]))
                       result-maps))
        results (mapv (comp :mu second) point->result-sorted-by-time)]
    {:best-results (reduce (fn [acc x] (conj acc (max (last acc) x)))
                           [(first results)] (rest results))
     :results results}))

(defn datapoints->projection-data
  [datapoints features]
  (let [result-maps (point->results-map datapoints)
        point->result-sorted-by-time
        (sort-by (comp :time second)
                 (mapv (fn [[point {:keys [time] :as m}]]
                         (let [recent-time (last (sort time))]
                           [point
                            (select-keys
                              (assoc m :time recent-time)
                              [:time :mu])]))
                       result-maps))]
    (->> (keys features)
         (mapv (fn [f]
                 (let [f-kw (keyword f)
                       f-default (-> features f-kw :default)]
                 {f-kw
                  {:x (mapv (fn [[p _]] (get p f-kw f-default)) point->result-sorted-by-time)
                   :y (mapv (comp :mu second) point->result-sorted-by-time)}})))
         (into {}))))
