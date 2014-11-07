(ns webapp.demo-data
  (:refer-clojure :exclude [get set]))

(def data
  [{:uuid "demo1"
    :name "Demo 1"
    :schema-id "test"
    :tests [{:uuid 1
             :title "A/Z testing"
             :type :az
             :tabs [:convergence
                    :cost-function
                    :feature-importances]}
            {:uuid 2
             :title "A/B testing"
             :type :ab
             :tabs [:convergence
                    :cost-function]}]}
   {:uuid "demo2"
    :name "Demo 2"
    :schema-id "test2"
    :tests [{:uuid 2
             :title "A/C testing"
             :type :az
             :tabs [:convergence
                    :cost-function
                    :feature-importances]}
            {:uuid 3
             :title "A/D testing"
             :type :ab
             :tabs [:convergence
                    :cost-function]}]}])

(defn get
  [uuid]
  (first (filter (comp #{uuid} :uuid) data)))
