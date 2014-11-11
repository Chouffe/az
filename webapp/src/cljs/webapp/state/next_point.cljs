(ns webapp.state.next-point
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce next-point-ratom (reagent/atom {}))

(defn set
  [uuid point]
  (swap! next-point-ratom assoc-in [(keyword uuid)] point))

(defn get
  [uuid]
  (get-in @next-point-ratom [(keyword uuid)]))


