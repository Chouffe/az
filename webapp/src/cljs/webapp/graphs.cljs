(ns webapp.graphs
  (:require
    [reagent.core :as reagent]
    [webapp.utils :as utils]
    [goog.string :as gstring]
    [goog.string.format]))

(defn scatter-plot
  [{:keys [data width height xlabel ylabel
           xticks yticks path? lines]
    :or {width 500 height 400
         xticks 5 yticks 3
         xlabel "x" ylabel "y"
         path? false}}]
  ;; TODO: improve the ticks
  (let [xdata (mapv first data)
        ydata (mapv second data)
        margin {:left 40 :right 40 :top 40 :bottom 40
                :axis-x 30 :axis-y 20
                :label-x 40 :label-y 40}
        width (- width (:left margin) (:right margin))
        height (- height (:top margin) (:bottom margin))
        xmin (apply min xdata)
        xmax (apply max xdata)
        ymax (apply max ydata)
        ymin (apply min ydata)
        xscale (fn [x] (/ (* x width) (+ xmin xmax)))
        yscale (fn [y] (if (= 0 (- ymin ymax)) height (- height (/ (* y height) (+ ymin ymax)))))]
    [:svg {:width (+ width (:left margin) (:right margin))
           :height (+ height (:top margin) (:bottom margin))}
     [:g.chart-area
      {:transform (str "translate(" (:left margin) "," (:top margin) ")")}
      (when lines
        [:g
         (for [{:keys [x y color line-width title dasharray]
                :or {dahsarray 0}} lines]
           (let [[x1 y1 x2 y2] (if y
                                 [0 (yscale y) width (yscale y)]
                                 [(xscale x) 0  (xscale x) height])]

             [:line {:style {"stroke" color
                             "stroke-dasharray" dasharray
                             "stroke-width" line-width}
                     :y1 y1 :x1 x1 :y2 y2 :x2 x2}]))])
      [:g
       (for [x (range xmin xmax (int (/ (- xmax xmin) xticks)))]
         [:g.ticks

          [:line {:style {"stroke" "#ccc" "stroke-width" 1}
                  :x1 (xscale x) :y1 0 :x2 (xscale x) :y2 height}]
          [:text {:x (xscale x)  :y (+ height (:axis-y margin))}
           x]])]
      [:g
       (when-not (= 0 (- ymax ymin))
         (for [y (range ymin ymax (/ (- ymax ymin) yticks))]
           [:g.ticks
            [:line {:style {"stroke" "#ccc" "stroke-width" 1}
                    :x1 0 :y1 (yscale y) :x2 width :y2 (yscale y)}]
            [:text {:x (- 0 (:axis-x margin)) :y (yscale y)}
             ;; TODO: fixme
             ;; y
             (gstring/format "%.1f" y)]]))]
      [:g.domain.domain-y
       [:line {:style {"stroke" "black" "stroke-width" 2}
               :x1 0 :y1 0 :x2 0 :y2 height}]
       [:text {:y -30 :x -20 :transform "rotate(270)"}
        ylabel]]
      [:g.domain.domain-x {:transform (str "translate(0," height ")")}
       [:line {:style {"stroke" "black" "stroke-width" 2}
               :x1 0 :y1 0 :x2 width :y2 0}]
       [:text {:x width
               :y (:label-x margin)}
        xlabel]]
      (when (and path? (seq xdata) (seq ydata))
        ;; (print ylabel)
        ;; (print xdata)
        ;; (print ydata)
        (let [path-string-start
              (str "M" (xscale (first xdata))
                   "," (yscale (first ydata)))

              path-string-middle
              (mapv (fn [[x y]] (str "L" (xscale x) "," (yscale y)))
                    data)]
          [:path {:style {"fill" "none"
                          "stroke" "#999"
                          "stroke-width" 1}
                  :d (str path-string-start
                          (apply str path-string-middle))}]))
      [:g.scatter
       (for [[x y] data]
         [:circle {:cx (xscale x)
                   :cy (yscale y)
                   :r 3
                   :style {"stroke" "black"
                           "stroke-width" 1
                           "fill" "#339CFF"}}])]]]))

(defn single-graph-comp
  ([ylabel ydata] (single-graph-comp ylabel ydata false))
  ([ylabel ydata dropping?]
  (let [display-info-line? (reagent/atom false)]
    (fn []
      (let [data (mapv vector (range) ydata)
            learning-limit 50
            ydata-learning (if dropping? (drop learning-limit ydata) ydata)
            std (utils/std ydata-learning)
            mean (utils/mean ydata-learning)
            info-lines
            [{:color "green"
              :line-width 3
              :title "convergence"
              :y (utils/mean (drop 50 ydata))}
             {:color "green"
              :line-width 3
              :dasharray 10
              :title "convergence std"
              :y (+ mean std)}
             {:color "green"
              :line-width 3
              :dasharray 10
              :title "convergence std"
              :y (- mean std)}
             {:color "red"
              :line-width 3
              :title "learning"
              :x 50}]]
        [:div
         [:div {:on-click #(swap! display-info-line? not)}
          "Display Info"]
         [scatter-plot
          {:data data
           :width 500
           :height 400
           :lines (when @display-info-line? info-lines)
           :xlabel "Draw #"
           :ylabel (name ylabel)
           :path? true
           :xticks 5
           :yticks 6}]])))))
