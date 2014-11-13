(ns webapp.db.indexes
  (:require [monger.collection :as mc]
            [webapp.db.component :as db]))

(defn create-indexes
  []
  (mc/ensure-index db/db "datapoints" (array-map :uuid 1))
  (mc/ensure-index db/db "abdatapoints" (array-map :uuid 1))
  (mc/ensure-index db/db "schemas" (array-map :uuid 1) {:unique true}))

(defn drop-indexes
  []
  (mc/drop-index db/db "datapoints")
  (mc/drop-index db/db "abdatapoints")
  (mc/drop-index db/db "schemas"))
