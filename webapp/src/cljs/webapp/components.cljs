(ns webapp.components
  (:require [reagent.core :as reagent]
            [cljs.reader :as reader]
            [webapp.state.schemas :as schemas]
            [webapp.state.convergence :as convergence]
            [webapp.state.cost-function :as cost-function]
            [webapp.state.projection :as projection]
            [webapp.state.application :as application]
            [webapp.services :as srv]
            [webapp.utils :as utils]
            [webapp.demo-data :as demo-data]
            [webapp.state.feature-importances :as feature-importances]
            [webapp.graphs :as graphs]
            [dommy.core :as dommy :refer-macros [sel sel1]]))

(defn navbar
  []
  (reagent/create-class
    {:component-will-mount
     (fn [_] (srv/load-schemas))

     :render
     (fn [_]
       (let [active-tab (application/get-tab)
             experiments (sort-by :uuid (schemas/get))]
         [:nav.navbar.navbar-default
          [:div.container-fluid
           [:div.navbar-header
            [:a.navbar-brand {:href "#"} "A/Z Testing"]]
           [:div.collapse.navbar-collapse
            [:ul.nav.navbar-nav
             [:li
              (when (= :home active-tab)
                {:class "active"})
              [:a {:href "#"} "Home"]]
             [:li.dropdown
              (when (= :experiments active-tab)
                {:class "active"})
              [:a.dropdown-toggle
               {:data-toggle "dropdown" :href "#"}
               "Experiments "
               [:span.caret]]
              [:ul.dropdown-menu
               (for [{:keys [uuid]} experiments]
               [:li
                [:a {:href (str "#/experiments/results/" uuid)}
                 uuid]])
               [:li.divider]
               [:li
                [:a {:href (str "#/experiments/new")}
                 "New experiment"]]]]
             [:li.dropdown
              (when (= :demo-results active-tab)
                {:class "active"})
              [:a.dropdown-toggle
               {:data-toggle "dropdown" :href "#"}
               "Demos "
               [:span.caret]]
              [:ul.dropdown-menu
               (for [{:keys [uuid name]} demo-data/data]
                 [:li
                  [:a {:href (str "#/demo/" uuid)}
                   name]])]]]]]]))}))

(defn tabs
  [data]
  [:ul.nav.nav-tabs
   (for [{:keys [title href active? on-click]} data]
     ^{:key title}
     [:li
      (when active? {:class "active"})
      [:a {:on-click on-click :href href} title]])])

(defn schema-component
  [schema-id]
  (let [{:keys [features uuid] :as schema}
        (schemas/get schema-id)]
    (if-not schema
      [:div]
      [:div.panel.panel-default
       [:div.panel-heading "Schema for " uuid]
       ;; [:div.panel-body "Here is the schema of the experiment"]
       [:table.table.table-striped
        [:thead
         [:tr
          [:th "Name"]
          [:th "Distribution"]
          [:th "Default"]
          [:th "Params"]
          [:th "Actions"]]]
        [:tbody
         (for [[feature-name feature-map] (sort-by key features)]
           ^{:key feature-name}
           (let [{:keys [default distribution params]} feature-map]
             [:tr
              [:td (name feature-name)]
              [:td distribution]
              [:td default]
              [:td (pr-str params)]
              [:td
               [:button.btn.btn-danger
                {:on-click #(srv/delete-feature uuid feature-name)}
                "Delete"]]]))]
        [:tfoot
         (let [distributions ["binary"
                              "uniform"
                              "uniform_discrete"
                              "normal"]]
           [:tr
            [:td
             [:input.form-control {:placeholder "Feature Name"
                                   :name "name"
                                   :id "feature-name"
                                   :required "required"}]]
            [:td
             [:select.form-control {:name "distribution"
                                    :id "feature-distribution"
                                    :required "required"}
              (for [distribution distributions]
                ^{:key distribution}
                [:option {:value distribution} distribution])]]
            [:td
             [:input.form-control {:placeholder "Default"
                                   :name "default"
                                   :id "feature-default"
                                   :required "required"}]]
            [:td
             [:input.form-control {:placeholder "Parameters"
                                   :id "feature-params"
                                   :name "params"
                                   :required "required"}]]
            [:td
             [:button.btn.btn-primary
              ;; TODO: feature map
              {:on-click #(let [name (dommy/value (sel1 :#feature-name))
                                distribution (dommy/value (sel1 :#feature-distribution))
                                default (dommy/value (sel1 :#feature-default))
                                params (reader/read-string (dommy/value (sel1 :#feature-params)))]
                            (srv/add-feature uuid name
                                             {:distribution distribution
                                              :default default
                                              :params (into {} (map (fn [[k v]] [(keyword k) v]) params))}))}
              "Add"]]])]]])))

(defn panel-comp
  [{:keys [title body footer]}]
  [:div.panel.panel-info
   [:div.panel-heading
    [:h3.panel-title title]]
   [:div.panel-body body]
   [:div.panel-footer footer]])

(defn graph-feature-importances
  [schema-id]
  (reagent/create-class
    {:component-will-mount
     (fn [_] (srv/load-feature-importances schema-id))

     :render
     (fn [_]
       (let [data (sort-by first < (feature-importances/get schema-id))]
         [:div
          (when data
            [graphs/bar-chart
             {:data (utils/scale-for-bar-charts data)}])]))}))

(defn graph-projection
  [schema-id]
  (reagent/create-class
    {:component-will-mount
     (fn [_] (srv/load-projection schema-id))

     :render
     (fn [_]
       (let [data (sort-by first < (projection/get schema-id))]
         [:div
          (for [[xlabel {:keys [x y]}] data]
            ^{:key xlabel}
            (if-not (pos? (count x))
              [:div]
              [graphs/scatter-plot
               {:data (mapv vector x y)
                :ylabel (str "f(" (name xlabel) ")")
                :xlabel (name xlabel)
                :width 500
                :height 400}]))]))}))

(defn graph-convergence
  [schema-id]
  (reagent/create-class
    {:component-will-mount
     (fn [_] (srv/load-convergence schema-id))

     :render
     (fn [_]
       (let [data (sort-by first < (convergence/get schema-id))]
       [:div
        (for [[ylabel ydata] data]
          ^{:key ylabel}
          (if (pos? (count ydata))
            [graphs/single-graph-comp ylabel ydata true]
            [:div]))]))}))

(defn graph-cost-function
  [schema-id]
  (reagent/create-class
    {:component-will-mount
     (fn [_] (srv/load-cost-function schema-id))

     :render
     (fn [_]
       (let [{:keys [results best-results]} (cost-function/get schema-id)]
         [:div
          (when results
            [graphs/scatter-plot
             {:data (mapv vector (range) results)
              :ylabel "F"
              :xlabel "time"
              ;; TODO: kill
              ;; :ymin 0
              ;; :ymax 0.25
              :lines [{:color "red"
                       :line-width 3
                       :title "learning"
                       :x 50}]
              :path? true}])
          (when best-results
            [graphs/scatter-plot
             {:data (mapv vector (range) best-results)
              :ylabel "Best F"
              :xlabel "time"
              ;; TODO kill
              ;; :ymin 0
              ;; :ymax 0.25
              :lines [{:color "red"
                       :line-width 3
                       :title "learning"
                       :x 50}]
              :path? true}])]))}))
