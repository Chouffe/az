(ns webapp.demo-data
  (:refer-clojure :exclude [get set]))

(def data
  [{:uuid "demo1"
    :name "Demo 1"
    :schema-id "lp"
    :tests [{:uuid 1
             :title "A/Z testing"
             :type :az
             :tabs [:convergence
                    :projection
                    :cost-function
                    :feature-importances]}
            {:uuid 2
             :title "A/B testing"
             :type :ab
             :tabs [:ab-convergence
                    :ab-cost-function]}]}
   {:uuid "demo2"
    :name "Demo 2"
    :schema-id "lp2"
    :tests [{:uuid 2
             :title "A/Z testing"
             :type :az
             :tabs [:convergence
                    :cost-function
                    :feature-importances]}
            {:uuid 3
             :title "A/B testing"
             :type :ab
             :tabs [:ab-convergence
                    :ab-cost-function]}]}])

(defn get
  [uuid]
  (first (filter (comp #{uuid} :uuid) data)))

(defn get-test
  [uuid-demo uuid-test]
  (first (filter (comp #{uuid-test} :uuid) (:tests (get uuid-demo)))))
