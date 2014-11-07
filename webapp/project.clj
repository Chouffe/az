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
                                   :optimizations :none
                                   :source-map true}}]}

  :profiles {:dev
             {:dependencies [;; CLJS
                             [org.clojure/clojurescript "0.0-2322"]
                             [figwheel "0.1.5-SNAPSHOT"]
                             [prismatic/dommy "1.0.0"]
                             [secretary "1.2.0"]
                             [reagent "0.4.2"]]
              :plugins [;; Clojurescript plugins
                        [lein-cljsbuild "1.0.3"] ;; 1.0.3 is a requirement
                        [lein-figwheel "0.1.5-SNAPSHOT"]]}}
  :source-paths ["src/clj"]
  :dependencies [[org.clojure/clojure "1.6.0"]])
