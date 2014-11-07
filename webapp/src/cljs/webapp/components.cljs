(ns webapp.components
  (:require [reagent.core :as reagent]
            [webapp.state.application :as application]
            [webapp.services :as srv]))

(defn navbar
  []
  (let [active-tab (application/get-tab)]
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
        [:li
         (when (or (= :demo active-tab)
                   (= :demo-results active-tab))
           {:class "active"})
         [:a {:href "#/demo"} "Demos"]]]]]]))

(defn tabs
  [data]
  [:ul.nav.nav-tabs
   (for [{:keys [title href active? on-click]} data]
     ^{:key title}
     [:li
      (when active? {:class "active"})
      [:a {:on-click on-click :href href} title]])])

(defn schema-component
  [{:keys [features uuid] :as schema}]
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
           [:td feature-name]
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
                                :required "required"}]]
         [:td
          [:select.form-control {:name "distribution"
                                 :required "required"}
           (for [distribution distributions]
             ^{:key distribution}
             [:option {:value distribution} distribution])]]
         [:td
          [:input.form-control {:placeholder "Default"
                                :name "default"
                                :required "required"}]]
         [:td
          [:input.form-control {:placeholder "Parameters"
                                :name "params"
                                :required "required"}]]
         [:td
          [:button.btn.btn-primary
           ;; TODO: feature map
           {:on-click #(srv/add-feature uuid {})}
           "Add"]]])]]])
