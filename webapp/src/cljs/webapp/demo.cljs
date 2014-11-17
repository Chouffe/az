(ns webapp.demo
  (:require [reagent.core :as reagent]
            [webapp.state.schemas :as schemas]
            [webapp.state.convergence :as convergence]
            [webapp.state.ab-convergence :as ab-convergence]
            [webapp.state.cost-function :as cost-function]
            [webapp.state.ab-cost-function :as ab-cost-function]
            [webapp.state.feature-importances :as feature-importances]
            [webapp.state.projection :as projection]
            [webapp.state.demo :as demo]
            [secretary.core :as secretary]
            [webapp.demo-data :as demo-data]
            [webapp.graphs :as graphs]
            [webapp.utils :as utils]
            [webapp.services :as srv]
            [dommy.core :as dommy :refer-macros [sel sel1]]
            [webapp.components :as components]))

(defn tabs-data
  [uuid active-tab tab-kw]
  (when (#{:convergence
           :cost-function
           :feature-importances
           :projection
           :ab-convergence
           :ab-cost-function}
                        tab-kw)
    (let [m {:on-click #(demo/set-tab uuid tab-kw)
             :active? (= active-tab tab-kw)}]
      (case tab-kw
        :projection (assoc m :title "Projection")
        :convergence (assoc m :title "Convergence")
        :ab-convergence (assoc m :title "Convergence")
        :cost-function (assoc m :title "Cost Function")
        :ab-cost-function (assoc m :title "Cost Function")
        :feature-importances (assoc m :title "Feature Importances")))))

;; TODO: move to components.cljs
(defn demo-graph-cost-function
  []
  (reagent/create-class
    {:component-will-mount
     (fn [_]
       (let [{:keys [schema-id]} (demo-data/get (demo/get-uuid))]
         (srv/load-cost-function schema-id)))

     :render
     (fn [_]
       (let [{:keys [schema-id]} (demo-data/get (demo/get-uuid))
             ydata (cost-function/get schema-id)]
         ;; TODO: kill + 3
         [:div
          (when ydata
            [graphs/scatter-plot
             {:data (mapv vector (range) ydata)
              :ylabel "F"
              :xlabel "time"
              :lines [{:color "red"
                       :line-width 3
                       :title "learning"
                       :x 50}]
              :path? true}])]))}))

(defn demo-graph-ab-cost-function
  []
  (reagent/create-class
    {:component-will-mount
     (fn [_]
       (let [{:keys [schema-id]} (demo-data/get (demo/get-uuid))]
         (srv/load-ab-cost-function schema-id)))

     :render
     (fn [_]
       (let [{:keys [schema-id]} (demo-data/get (demo/get-uuid))
             ydata (ab-cost-function/get schema-id)]
         ;; TODO: kill + 3
         [:div
          (when ydata
            [graphs/scatter-plot
             {:data (mapv vector (range) ydata)
              :ylabel "F"
              :xlabel "time"
              :path? true}])]))}))

(defn demo-graph-convergence
  []
  (reagent/create-class
    {:component-will-mount
     (fn [_]
       (let [{:keys [schema-id]} (demo-data/get (demo/get-uuid))]
         (srv/load-convergence schema-id)))

     :render
     (fn [_]
       (let [{:keys [schema-id]} (demo-data/get (demo/get-uuid))]
         [:div
          (for [[ylabel ydata] (convergence/get schema-id)]
            ^{:key ylabel}
            [graphs/single-graph-comp ylabel ydata true])]))}))

(defn demo-graph-ab-convergence
  []
  (reagent/create-class
    {:component-will-mount
     (fn [_]
       (let [{:keys [schema-id]} (demo-data/get (demo/get-uuid))]
         (srv/load-ab-convergence schema-id)))

     :render
     (fn [_]
       (let [{:keys [schema-id]} (demo-data/get (demo/get-uuid))]
         [:div
          (for [[ylabel ydata] (sort-by first < (ab-convergence/get schema-id))]
            ^{:key ylabel}
            [graphs/single-graph-comp ylabel ydata])]))}))

(defn demo-graph
  [uuid]
  (let [active-tab (demo/get-tab uuid)
        {:keys [schema-id]} (demo-data/get (demo/get-uuid))]
    (case active-tab
      :convergence
      [components/graph-convergence schema-id]

      :ab-convergence
      [demo-graph-ab-convergence]

      :cost-function
      [components/graph-cost-function schema-id]

      :ab-cost-function
      [demo-graph-ab-cost-function]

      :projection
      [components/graph-projection schema-id]

      :feature-importances
      [components/graph-feature-importances schema-id]

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
  (reagent/create-class
    {:component-did-mount
     (fn [_]
       (let [demo-uuid (demo/get-uuid)
             {:keys [schema-id]} (demo-data/get demo-uuid)]
         (srv/load-schema schema-id)))

     :render
     (fn [_]
       (let [demo-uuid (demo/get-uuid)
             {:keys [schema-id tests] :as demo}
             (demo-data/get demo-uuid)]
         [:div.container
          ;; TODO: FIXME
          #_[:div.center-block
           [:button.btn.btn-success.btn-lg
            {:on-click #(srv/run-demo demo-uuid)}
            "Run"]]
          [components/schema-component schema-id]
          [:div.row
           (for [{:keys [uuid] :as test} tests]
             ^{:key uuid}
             [demo-results-test-comp test])]]))}))
