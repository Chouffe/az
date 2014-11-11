(ns webapp.experiments
  (:require [reagent.core :as reagent]
            [clojure.string :as string]
            [cljs.reader :as reader]
            [dommy.core :as dommy :refer-macros [sel sel1]]
            [webapp.state.schemas :as schemas]
            [webapp.state.convergence :as convergence]
            [webapp.state.application :as application]
            [webapp.state.projection :as projection]
            [webapp.state.feature-importances :as feature-importances]
            [webapp.state.experiments :as experiments]
            [webapp.state.next-point :as next-point]
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
             ^{:key i}
             [:tr
              [:td
               [:input.form-control
                {:name "feature-name" :required true}]]
              [:td
               [:select.form-control
                {:name "feature-distribution" :required true}
                (for [distribution ["binary" "uniform" "uniform_discrete" "normal"]]
                  ^{:key distribution}
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

(defn tabs-data
  [uuid active-tab tab-kw]
  (when (#{:convergence
           :feature-importances
           :projection} tab-kw)
    (let [m {:on-click #(experiments/set-tab uuid tab-kw)
             :active? (= active-tab tab-kw)}]
      (case tab-kw
        :projection (assoc m :title "Projection")
        :convergence (assoc m :title "Convergence")
        :feature-importances (assoc m :title "Feature Importances")))))

(defn experiment-graph
  [uuid]
  (let [active-tab (experiments/get-tab uuid)]
    (case active-tab
      :convergence
      [components/graph-convergence uuid]

      :projection
      [components/graph-projection uuid]

      :feature-importances
      [components/graph-feature-importances uuid]

      [:div "Select a tab..."])))

(defn experiment-results-comp
  []
  (let [tabs [:convergence :projection :feature-importances]]
  (reagent/create-class
    {:component-will-mount
     (fn [_] (do
               (experiments/set-tab (experiments/get-uuid) (first tabs))
               (srv/get-next-point (experiments/get-uuid))))

     :render
     (fn [_]
       (let [uuid (experiments/get-uuid)
             api-url "http://localhost:5002/api/"
             active-tab (experiments/get-tab uuid)
             next-point (next-point/get uuid)
             next-point-result (assoc next-point :result 42)]
         [:div.container
          (when uuid
            [components/schema-component uuid])
          (when next-point
            [:div
             [components/panel-comp
              {:title "Next point to try"
               :body (pr-str (next-point/get uuid))
               :footer (str "$ curl " api-url uuid)}]
             [components/panel-comp
              {:title "Save a result"
               :body (pr-str (assoc (next-point/get uuid) :result 42))
               :footer (str "$ curl -X POST -H \"Content-Type: application/json\" -d " next-point-result " " api-url uuid)}]])

          [components/tabs (mapv (partial tabs-data uuid active-tab) tabs)]
          [experiment-graph uuid]]))})))
