(ns webapp.state.feature-importances
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce feature-importances-ratom (reagent/atom {}))

(defn set
  [uuid data]
  ;; (reset! schema-ratom {uuid schema})
  (swap! feature-importances-ratom assoc-in [(keyword uuid)] data))

(defn get
  [uuid]
  (get-in @feature-importances-ratom [(keyword uuid)]))


