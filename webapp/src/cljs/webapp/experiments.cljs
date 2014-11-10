(ns webapp.experiments
  (:require [reagent.core :as reagent]
            [webapp.state.schemas :as schemas]
            [webapp.state.convergence :as convergence]
            [webapp.state.application :as application]
            [webapp.components :as components]
            [webapp.routes :as routes]
            [webapp.graphs :as graphs]
            [webapp.services :as srv]
            [webapp.utils :as utils]))


(defn experiments-comp
  []
  [:div.container
   [:div
   "Set up a new experiment here"]])

(defn experiment-results-comp
  []
  (print "TEEEST")
  [:div.container
   [:div "RESULTS"]])


