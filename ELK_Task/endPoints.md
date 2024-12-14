# Elasticsearch Endpoints Documentation

## Endpoint 1: **Class Distribution**

- **Purpose**:
  - Retrieve the distribution of classes (e.g., `digit`, `month`) within the annotations.
  - Useful for understanding the diversity and frequency of annotation classes.

- **Query**:
  ```
  GET /labeled_images_ziad_abdlhamed/_search
  {
    "size": 0,
    "aggs": {
      "class_distribution": {
        "nested": { "path": "annotations" },
        "aggs": {
          "classes": {
            "terms": { "field": "annotations.class" }
          }
        }
      }
    }
  }
  ```

- **Example Response**:
  ```
  {
    "aggregations": {
      "class_distribution": {
        "doc_count": 100,
        "classes": {
          "buckets": [
            { "key": "digit", "doc_count": 80 },
            { "key": "month", "doc_count": 20 }
          ]
        }
      }
    }
  }
  ```

## Endpoint 2: **Label Distribution**

- **Purpose**:
  - Identify the most frequent labels (e.g., `Two`, `August`) across all annotations.
  - Helps highlight the common numbers or months within the dataset.

- **Query**:
  ```
  GET /labeled_images_ziad_abdlhamed/_search
  {
    "size": 0,
    "aggs": {
      "label_distribution": {
        "nested": { "path": "annotations" },
        "aggs": {
          "labels": {
            "terms": { "field": "annotations.label" }
          }
        }
      }
    }
  }
  ```

- **Example Response**:
  ```
  {
    "aggregations": {
      "label_distribution": {
        "doc_count": 100,
        "labels": {
          "buckets": [
            { "key": "Two", "doc_count": 40 },
            { "key": "August", "doc_count": 30 },
            { "key": "Three", "doc_count": 20 }
          ]
        }
      }
    }
  }
  ```

## Endpoint 3: **Trends Over Time**

- **Purpose**:
  - Visualize annotation activity over time, grouped by months.
  - Useful for monitoring data creation patterns.

- **Query**:
  ```
  GET /labeled_images_ziad_abdlhamed/_search
  {
    "size": 0,
    "aggs": {
      "annotations_over_time": {
        "date_histogram": {
          "field": "timestamp",
          "calendar_interval": "month"
        }
      }
    }
  }
  ```

- **Example Response**:
  ```
  {
    "aggregations": {
      "annotations_over_time": {
        "buckets": [
          { "key_as_string": "2024-01-01", "doc_count": 10 },
          { "key_as_string": "2024-02-01", "doc_count": 20 },
          { "key_as_string": "2024-03-01", "doc_count": 30 }
        ]
      }
    }
  }
  ```

## Endpoint 4: **Most Frequent Label**

- **Purpose**:
  - Determine the single most frequent label across all annotations.
  - Useful for identifying dominant patterns in the dataset.

- **Query**:
  ```
  GET /labeled_images_ziad_abdlhamed/_search
  {
    "size": 0,
    "aggs": {
      "most_frequent_label": {
        "terms": {
          "field": "annotations.label",
          "size": 1,
          "order": { "_count": "desc" }
        }
      }
    }
  }
  ```

- **Example Response**:
  ```
  {
    "aggregations": {
      "most_frequent_label": {
        "buckets": [
          { "key": "Two", "doc_count": 50 }
        ]
      }
    }
  }
  ```

## Endpoint 5: **Records with Annotations**

- **Purpose**:
  - Retrieve all records containing annotations, ensuring no missing data.

- **Query**:
  ```
  GET /labeled_images_ziad_abdlhamed/_search
  {
    "query": {
      "exists": { "field": "annotations" }
    }
  }
  ```

- **Example Response**:
  ```
  {
    "hits": {
      "total": { "value": 21 },
      "hits": [
        { "_source": { "image_name": "image1.jpg", "annotations": [...] } },
        { "_source": { "image_name": "image2.jpg", "annotations": [...] } }
      ]
    }
  }
  ```

## Endpoint 6: **Number Frequency**

- **Purpose**:
  - Count the frequency of each numeric label in the dataset.

- **Query**:
  ```
  GET /labeled_images_ziad_abdlhamed/_search
  {
    "size": 0,
    "aggs": {
      "number_frequency": {
        "terms": {
          "field": "annotations.label",
          "size": 10
        }
      }
    }
  }
  ```

- **Example Response**:
  ```
  {
    "aggregations": {
      "number_frequency": {
        "buckets": [
          { "key": "Two", "doc_count": 40 },
          { "key": "Three", "doc_count": 20 },
          { "key": "Eight", "doc_count": 10 }
        ]
      }
    }
  }
  ```

---

### Summary
This documentation outlines the key Elasticsearch queries and endpoints used in the project. Each query is crafted to extract meaningful insights, such as class distributions, label frequencies, and trends over time. These endpoints are essential for analyzing the labeled image dataset effectively and providing actionable insights.