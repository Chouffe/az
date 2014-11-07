(ns webapp.demo
  (:require [reagent.core :as reagent]
            [webapp.state.schemas :as schemas]
            [webapp.state.demo :as demo]
            [secretary.core :as secretary]
            [webapp.demo-data :as demo-data]
            [webapp.utils :as utils]
            [dommy.core :as dommy :refer-macros [sel sel1]]
            [webapp.components :as components]))

(defn demo-comp
  []
  [:div.container
   [:div.jumbotron
    [:h1 "Demos"]
    [:p "Select the demo you want to run :)"]
    [:div.input-group
     [:select.form-control
      (for [{:keys [uuid name]} demo-data/data]
        [:option {:value uuid} name])]
     [:span.input-group-btn
      [:button.btn.btn-success
       {:id "yo"
        :on-click
        #(let [selected-demo (dommy/value (sel1 :select))]
           (secretary/dispatch! (str "/demo/" selected-demo))
           (print selected-demo))}
       "Run"]]]]])

(defn tabs-data
  [uuid active-tab tab-kw]
  (when (#{:convergence :cost-function :feature-importances} tab-kw)
    (let [m {:on-click #(demo/set-tab uuid tab-kw)
             :active? (= active-tab tab-kw)}]
      (case tab-kw
        :convergence (assoc m :title "Convergence")
        :cost-function (assoc m :title "Cost Function")
        :feature-importances (assoc m :title "Feature Importances")))))

(defn demo-graph
  [uuid]
  (let [active-tab (demo/get-tab uuid)]
    (case active-tab
      :convergence
      [:div "Convergence"]

      :cost-function
      [:div  "Cost Function"]

      :feature-importances
      [:div "Feature Importances"]

      [:div "Select a tab..."])))

(defn demo-results-test-comp
  [{:keys [uuid tabs title] :as test}]
  (reagent/create-class
    {:component-will-mount
     (fn [_] (demo/set-tab uuid (first tabs)))

     :render
     (fn [_]
       (let [active-tab (demo/get-tab uuid)]
         [:div.col-md-6
          [:h2 title]
          [components/tabs (mapv (partial tabs-data uuid active-tab) tabs)]
          [demo-graph uuid]]))}))

(defn demo-results-comp
  []
  (let [demo-uuid (demo/get-uuid)
        {:keys [schema-id tests] :as demo}
        (demo-data/get demo-uuid)]
    [:div.container
     [components/schema-component (schemas/get "test")]
     [:div.row
      (for [{:keys [uuid] :as test} tests]
        ^{:key uuid}
        [demo-results-test-comp test])]]))
