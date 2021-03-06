(ns webapp.state.ab-cost-function
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce ab-cost-function-ratom (reagent/atom {}))

(defn set
  [uuid data]
  (swap! ab-cost-function-ratom assoc-in [(keyword uuid)] data))

(defn delete
  [uuid]
  (swap! ab-cost-function-ratom dissoc (keyword uuid)))

(defn get
  [uuid]
  (get-in @ab-cost-function-ratom [(keyword uuid)]))


