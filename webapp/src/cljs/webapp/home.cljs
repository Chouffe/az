(ns webapp.home
  (:require [reagent.core :as reagent]
            [webapp.state.schemas :as schemas]
            [webapp.state.convergence :as convergence]
            [webapp.state.application :as application]
            [webapp.components :as components]
            [webapp.routes :as routes]
            [webapp.graphs :as graphs]
            [webapp.services :as srv]
            [webapp.utils :as utils]
            [figwheel.client :as fw :include-macros true]))


(defn home-comp
  []
  (reagent/create-class
    {:component-will-mount
     (fn [_] (srv/load-convergence "lp"))

     :render
     (fn [_] [:div.container "HELLO"])}))
