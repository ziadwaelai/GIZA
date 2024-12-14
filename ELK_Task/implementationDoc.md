# Implementation Documentation

## Data Ingestion

### Steps
1. **Prepare Data**:
   - Organized labeled image data in JSON format with `image_name`, `timestamp`, and nested `annotations` containing `label`, `class`, and `coordinates`.

2. **Create the Index**:
   - Used this mapping to define the index:
     ```
     PUT /labeled_images_ziad_abdlhamed
     {
       "mappings": {
         "properties": {
           "image_name": { "type": "keyword" },
           "timestamp": { "type": "date" },
           "annotations": {
             "type": "nested",
             "properties": {
               "label": { "type": "keyword" },
               "class": { "type": "keyword" },
               "coordinates": {
                 "type": "object",
                 "properties": {
                   "x": { "type": "float" },
                   "y": { "type": "float" },
                   "width": { "type": "float" },
                   "height": { "type": "float" }
                 }
               }
             }
           }
         }
       }
     }
     ```

3. **Insert Data**:
   - Indexed the data using the `_bulk` API.
   - Example:
     ```
     POST /labeled_images_ziad_abdlhamed/_bulk
     { "index": {} }
     {
       "image_name": "image1.jpg",
       "timestamp": "2024-12-10T09:33:17+00:00",
       "annotations": [
         { "label": "Two", "class": "digit", "coordinates": { "x": 100, "y": 200, "width": 50, "height": 100 } }
       ]
     }
     ```

---

## Mapping Decisions

1. **`image_name`**:
   - Type: `keyword` (unique identifier for filtering).
2. **`timestamp`**:
   - Type: `date` (for time-based trends).
3. **`annotations`**:
   - Type: `nested` (allows querying individual annotations).
4. **Subfields of `annotations`**:
   - `label` and `class`: `keyword` (for categorical data).
   - `coordinates`: `float` (numerical bounding box data).

---

## Query Design

1. **Class Distribution**:
   - Query:
     ```
     GET /labeled_images_ziad_abdlhamed/_search
     {
       "size": 0,
       "aggs": {
         "class_distribution": {
           "nested": { "path": "annotations" },
           "aggs": { "classes": { "terms": { "field": "annotations.class" } } }
         }
       }
     }
     ```
   - Purpose: Count each class type (e.g., `digit`).

2. **Label Distribution**:
   - Query:
     ```
     GET /labeled_images_ziad_abdlhamed/_search
     {
       "size": 0,
       "aggs": {
         "label_distribution": {
           "nested": { "path": "annotations" },
           "aggs": { "labels": { "terms": { "field": "annotations.label" } } }
         }
       }
     }
     ```
   - Purpose: Find most common labels (e.g., `Two`).

3. **Trends Over Time**:
   - Query:
     ```
     GET /labeled_images_ziad_abdlhamed/_search
     {
       "size": 0,
       "aggs": {
         "annotations_over_time": {
           "date_histogram": { "field": "timestamp", "calendar_interval": "month" }
         }
       }
     }
     ```
   - Purpose: Track annotation activity by month.

4. **Most Frequent Label**:
   - Query:
     ```
     GET /labeled_images_ziad_abdlhamed/_search
     {
       "size": 0,
       "aggs": {
         "most_frequent_label": {
           "terms": { "field": "annotations.label", "size": 1, "order": { "_count": "desc" } }
         }
       }
     }
     ```
   - Purpose: Identify the most frequent label.

---

## Visualization Choices

1. **Most Frequent Numbers**:
   - **Type**: Bar chart.
   - **Purpose**: Show frequency of numeric labels.

2. **Most Frequent Class**:
   - **Type**: Metric visualization.
   - **Purpose**: Highlight the top class (e.g., `digit`).

3. **Annotations Over Time**:
   - **Type**: Line chart.
   - **Purpose**: Show trends in annotation activity.

4. **Total Records**:
   - **Type**: Metric visualization.
   - **Purpose**: Display total images processed.

5. **Average Coordinates (X, Y)**:
   - **Type**: Metric visualization.
   - **Purpose**: Show average spatial distribution.

---

## Summary

- Data ingestion and mapping ensured accurate structure and query capability.
- Queries were designed to analyze key metrics, such as label and class distributions.
- The dashboard provides clear insights into the dataset through relevant visualizations.

