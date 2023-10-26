import src.data_fetcher as data_fetcher
import src.pre_processor as preprocessor
import src.data_explorer as data_explorer
import src.filter as filter
import src.sentiment_analyser as sentiment_analyser
import src.topic_modeler as topic_modeler
import src.visualizer as visualizer

if __name__ == "__main__":

    # config
    visualize = True

    # get data
    # data = data_fetcher.fetch(data_points_per_district=1000)
    data = data_fetcher.aggregate()
    print("data loaded")

    # very basic preprocessing
    data = preprocessor.process(data)
    print("pre processed")

    # exploratory data analysis
    # data_explorer.explore_data(data)
    #data_explorer.topic_model(data)
    #for i in [5, 10, 15]:
        #topic_modeler.get_topics(data['Pre_Processed'].tolist(), i)
    print("basic topic model created")

    # filter out irrelevant tweets
    data = filter.filter(data)

    # pre-processing for sentiment analysis

    # sentiment analysis
    data = sentiment_analyser.get_sentiments(data)
    data_for_vis_month, data_for_vis_week, data_for_vis_overview = sentiment_analyser.aggregate_sentiments_for_visualization(data)
    print("sentiments calculated")
    # pre-processing for topic models

    # topic models
    ####topic_modeler.get_topics_per_district(data)

    # save figures to folder
    if visualize:
        visualizer.create_interactive_map()
        visualizer.visualize_total_sentiment_per_week(data_for_vis_overview)
        visualizer.visualize_sentiment_maps_month(data_for_vis_month)
        visualizer.visualize_sentiment_maps_week(data_for_vis_week)

        print("visualization finished")

    print("done")


