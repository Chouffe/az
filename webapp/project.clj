(defproject webapp "0.1.0-SNAPSHOT"
  :description "A/Z Testing webapp"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :figwheel {:css-dirs ["resources/public/css"]}
  :cljsbuild {:builds [{:id "dev"
                        :source-paths ["src/cljs"]
                        :compiler {:output-to "resources/public/js/compiled/webapp.js"
                                   :output-dir "resources/public/js/compiled/out"
                                   :preamble ["reagent/react.js"]
                                   :externs ["react/externs/react.js"]

                                   :libs ["singult.js"]
                                   :optimizations :none
                                   :source-map true}}]}

  :profiles {:dev
             {:dependencies [;; CLJS
                             [org.clojure/clojurescript "0.0-2322"]
                             [figwheel "0.1.5-SNAPSHOT"]
                             [prismatic/dommy "1.0.0"]
                             [cljs-http "0.1.20"]
                             [org.clojure/core.async "0.1.346.0-17112a-alpha"]
                             [secretary "1.2.0"]
                             [reagent "0.4.2"]]
              :plugins [;; Clojurescript plugins
                        [lein-cljsbuild "1.0.3"] ;; 1.0.3 is a requirement
                        ;; [lein-cljsbuild "0.2.7"] ;; 1.0.3 is a requirement
                        [lein-figwheel "0.1.5-SNAPSHOT"]]}}
  :source-paths ["src/clj"]
  :main webapp.core
  :dependencies [[org.clojure/clojure "1.6.0"]
                 [org.clojure/tools.logging "0.3.0"]
                 [clj-http "1.0.1"]
                 [cheshire "5.3.1"]
                 [clj-time "0.8.0"]
                 [ring "1.3.1"]
                 [com.novemberain/monger "2.0.0"]
                 [com.stuartsierra/component "0.2.1"]
                 [ring/ring-json "0.3.1"]
                 [http-kit "2.1.18"]
                 [compojure "1.2.1"]])
