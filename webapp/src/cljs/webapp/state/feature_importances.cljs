(ns webapp.state.feature-importances
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce feature-importances-ratom (reagent/atom {}))

(defn set
  [uuid data]
  (swap! feature-importances-ratom assoc-in [(keyword uuid)] data))

(defn delete
  [uuid]
  (swap! feature-importances-ratom dissoc (keyword uuid)))

(defn get
  [uuid]
  (get-in @feature-importances-ratom [(keyword uuid)]))


