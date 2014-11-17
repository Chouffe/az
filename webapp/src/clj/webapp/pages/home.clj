(ns webapp.pages.home
  (:require [hiccup.core :as hiccup]))

(defn home-page
  []
  (hiccup/html
    (list
      "<!DOCTYPE html>"
      [:html
       [:head
        [:link {:rel "stylesheet" :href "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css"}]]
       [:body
        [:div#main-area]
        [:script {:type "text/javascript"
                  :src "https://code.jquery.com/jquery-2.1.1.min.js"}]
        [:script {:type "text/javascript"
                  :src "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"}]
        [:script {:type "text/javascript"
                  :src "http://fb.me/react-0.9.0.js"}]
        [:script {:type "text/javascript"
                  :src "js/compiled/out/goog/base.js"}]
        [:script {:type "text/javascript"
                  :src "js/compiled/webapp.js"}]
        [:script {:type "text/javascript"}
         "goog.require(\"webapp.core\");"]]])))
