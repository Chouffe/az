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
     (fn [_] #_(srv/load-convergence "lp"))

     :render
     (fn [_]
       [:div.container
        [graphs/bar-chart {:data (utils/scale-for-bar-charts {:a0 30 :a1 200 :a2 23 :b1 34 :c2 40 :b 40 :e 50 :f 69 :g 10})}]

        ])}))
