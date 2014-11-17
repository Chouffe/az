(ns webapp.state.projection
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce projection-ratom (reagent/atom {}))

(defn set
  [uuid data]
  (swap! projection-ratom assoc-in [(keyword uuid)] data))

(defn delete
  [uuid]
  (swap! projection-ratom dissoc (keyword uuid)))

(defn get
  [uuid]
  (get-in @projection-ratom [(keyword uuid)]))

