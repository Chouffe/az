(ns webapp.experiments
  (:require [reagent.core :as reagent]
            [clojure.string :as string]
            [cljs.reader :as reader]
            [dommy.core :as dommy :refer-macros [sel sel1]]
            [webapp.state.schemas :as schemas]
            [webapp.state.convergence :as convergence]
            [webapp.state.application :as application]
            [webapp.state.experiments :as experiments]
            [webapp.components :as components]
            [webapp.routes :as routes]
            [webapp.graphs :as graphs]
            [webapp.services :as srv]
            [webapp.utils :as utils]))


(defn experiments-comp
  []
  (let [num-features (reagent/atom 1)]
    (fn []
      [:div.container
       [:h1 "Create a new experiment"]
       [:form
        {:on-submit
        (utils/prevent-default
         #(let [form-data
                (->> (sel :.form-control)
                     (mapv (fn [elem] [(dommy/attr elem :name) (dommy/value elem)])))
                experiment-name (second (first form-data))
                feature-map
                (->> form-data
                     (drop 1)
                     (partition 4)
                     (mapv (fn [[[_ feature-name]
                                 [_ feature-distribution]
                                 [_ feature-default]
                                 [_ feature-params]]]
                             (let [params (when-not (string/blank? feature-params)
                                            (->> feature-params
                                                 reader/read-string
                                                 (map (fn [[k v]] [(keyword k) v]))
                                                 (into {})))
                                   default (if-not (string/blank? feature-default)
                                             feature-default
                                             0)]
                             {feature-name
                              (merge
                                {:distribution feature-distribution}
                                (when default {:params default})
                                (when params {:params params}))})))
                     (into {}))]
            (srv/create-schema experiment-name feature-map)))}
        [:div.form-group
         [:label {:for "name"} "Name"]
         [:input.form-control
          {:name "experiment-name"
           :autofocus true
           :required "required"}]]
        [:div.form-group
         [:label "Features"]
         [:a {:on-click #(swap! num-features inc)}
          "Add a feature"]
         [:a {:on-click #(swap! num-features (fn [x] (if (pos? x) (dec x) x)))}
          "Remove a feature"]
         [:table.table.table-striped.table-bordered
          [:thead
           [:tr
            [:th "Name"]
            [:th "Distribution"]
            [:th "Default"]
            [:th "Params"]]]
          [:tbody
           (for [i (range @num-features)]
             [:tr
              [:td
               [:input.form-control
                {:name "feature-name" :required true}]]
              [:td
               [:select.form-control
                {:name "feature-distribution" :required true}
                (for [distribution ["binary" "uniform" "uniform_discrete" "normal"]]
                  [:option {:value distribution}
                   distribution])]]
              [:td
               [:input.form-control
                {:name "feature-default" :required true}]]
              [:td
               [:input.form-control
                {:name "feature-params"}]]])]]]
        [:button.btn.btn-primary "Create"]]

       "Set up a new experiment here"])))

(defn experiment-results-comp
  []
  [:div.container
   [components/schema-component (experiments/get-uuid)]])


