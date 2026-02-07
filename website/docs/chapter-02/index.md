---
id: chapter-02
title: Sensors & Perception
sidebar_label: Chapter 2
sidebar_position: 3
description: Learn about sensor types, data processing, and computer vision for robotics
keywords: [sensors, perception, computer vision, robotics]
reading_time: 7
chapter_number: 2
learning_objectives:
  - Understand different types of sensors used in robotics
  - Learn how robots process sensor data
  - Explore computer vision fundamentals
key_takeaways:
  - Sensors are the eyes and ears of robots
  - Multiple sensor types provide complementary information
  - Computer vision enables robots to understand visual scenes
---

# Chapter 2: Sensors & Perception

*Estimated reading time: 7 minutes*

## Introduction to Robot Sensing

Robots rely on sensors to perceive their environment. Just as humans use sight, hearing, and touch, robots use various sensors to gather information about the world around them.

## Types of Sensors

### 1. Vision Sensors
- **Cameras**: RGB cameras capture visual information
- **Depth Cameras**: Measure distance to objects (e.g., Intel RealSense)
- **LIDAR**: Laser-based distance measurement for 3D mapping

### 2. Proximity Sensors
- **Ultrasonic**: Sound-based distance measurement
- **Infrared**: Detect nearby objects using IR light
- **Touch Sensors**: Detect physical contact

### 3. Motion Sensors
- **IMU (Inertial Measurement Unit)**: Measures acceleration and rotation
- **Encoders**: Track motor position and velocity
- **GPS**: Outdoor positioning

## Sensor Data Processing

Raw sensor data must be processed to extract useful information:

```python title="sensor_processing.py"
import numpy as np

class SensorProcessor:
    def __init__(self):
        self.sensor_data = []

    def process_camera_image(self, image):
        """Process camera image for object detection"""
        # Simplified example
        gray_image = self.convert_to_grayscale(image)
        edges = self.detect_edges(gray_image)
        return edges

    def convert_to_grayscale(self, image):
        """Convert RGB to grayscale"""
        return np.mean(image, axis=2)

    def detect_edges(self, image):
        """Simple edge detection"""
        # Placeholder for edge detection algorithm
        return image

# Example usage
processor = SensorProcessor()
```

## Computer Vision Basics

Computer vision enables robots to understand visual scenes:

- **Object Detection**: Identify and locate objects in images
- **Segmentation**: Separate objects from background
- **Pose Estimation**: Determine object orientation
- **Scene Understanding**: Comprehend spatial relationships

## Sensor Fusion

Combining data from multiple sensors provides more robust perception:

- **Complementary**: Different sensors cover each other's weaknesses
- **Redundancy**: Multiple sensors increase reliability
- **Accuracy**: Fusion improves measurement precision

## Key Takeaways

- Sensors are the eyes and ears of robots
- Multiple sensor types provide complementary information
- Computer vision enables robots to understand visual scenes
- Sensor fusion combines data for robust perception

---

## اردو ترجمہ (Urdu Translation)

# باب 2: سینسرز اور ادراک

*تخمینی پڑھنے کا وقت: 7 منٹ*

## روبوٹ سینسنگ کا تعارف

روبوٹس اپنے ماحول کو سمجھنے کے لیے سینسرز پر انحصار کرتے ہیں۔ جس طرح انسان بصارت، سماعت اور لمس استعمال کرتے ہیں، روبوٹس اپنے اردگرد کی دنیا کے بارے میں معلومات اکٹھا کرنے کے لیے مختلف سینسرز استعمال کرتے ہیں۔

## سینسرز کی اقسام

### 1. بصری سینسرز
- **کیمرے**: RGB کیمرے بصری معلومات کیپچر کرتے ہیں
- **ڈیپتھ کیمرے**: اشیاء تک فاصلہ ناپتے ہیں (مثلاً Intel RealSense)
- **لائیڈار**: 3D میپنگ کے لیے لیزر پر مبنی فاصلہ پیمائش

### 2. قربت کے سینسرز
- **الٹراسونک**: آواز پر مبنی فاصلہ پیمائش
- **انفراریڈ**: IR روشنی استعمال کرتے ہوئے قریبی اشیاء کا پتہ لگانا
- **ٹچ سینسرز**: جسمانی رابطے کا پتہ لگانا

### 3. حرکت کے سینسرز
- **IMU (Inertial Measurement Unit)**: تیزی اور گردش کی پیمائش کرتا ہے
- **انکوڈرز**: موٹر کی پوزیشن اور رفتار کو ٹریک کرتے ہیں
- **GPS**: بیرونی پوزیشننگ

## سینسر ڈیٹا کی پروسیسنگ

خام سینسر ڈیٹا کو مفید معلومات نکالنے کے لیے پروسیس کرنا ضروری ہے۔

## کمپیوٹر ویژن کی بنیادیں

کمپیوٹر ویژن روبوٹس کو بصری مناظر سمجھنے کے قابل بناتی ہے:

- **آبجیکٹ ڈیٹیکشن**: تصاویر میں اشیاء کی شناخت اور مقام کا تعین
- **سیگمنٹیشن**: پس منظر سے اشیاء کو الگ کرنا
- **پوز ایسٹیمیشن**: آبجیکٹ کی سمت کا تعین
- **منظر کی سمجھ**: مقامی تعلقات کو سمجھنا

## سینسر فیوژن

متعدد سینسرز سے ڈیٹا کو ملانا زیادہ مضبوط ادراک فراہم کرتا ہے:

- **تکمیلی**: مختلف سینسرز ایک دوسرے کی کمزوریوں کو پورا کرتے ہیں
- **فالتو پن**: متعدد سینسرز اعتبار میں اضافہ کرتے ہیں
- **درستگی**: فیوژن پیمائش کی درستگی کو بہتر بناتا ہے

## اہم نکات

- سینسرز روبوٹس کی آنکھیں اور کان ہیں
- متعدد سینسر اقسام تکمیلی معلومات فراہم کرتی ہیں
- کمپیوٹر ویژن روبوٹس کو بصری مناظر سمجھنے کے قابل بناتی ہے
- سینسر فیوژن مضبوط ادراک کے لیے ڈیٹا کو یکجا کرتا ہے

---

**Next:** [Chapter 3: Actuation & Control](../chapter-03/index.md) →
