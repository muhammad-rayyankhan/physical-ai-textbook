---
id: chapter-03
title: Actuation & Control
sidebar_label: Chapter 3
sidebar_position: 4
description: Explore motors, servos, and control systems for robotic movement
keywords: [actuation, control systems, motors, servos]
reading_time: 7
chapter_number: 3
learning_objectives:
  - Understand different types of actuators
  - Learn control system fundamentals
  - Explore motion planning concepts
key_takeaways:
  - Actuators convert electrical signals into physical motion
  - Control systems ensure precise and stable movement
  - Motion planning enables complex behaviors
---

# Chapter 3: Actuation & Control

*Estimated reading time: 7 minutes*

## Introduction to Actuation

Actuation is how robots move and interact with the physical world. Actuators convert electrical energy into mechanical motion.

## Types of Actuators

### 1. Electric Motors
- **DC Motors**: Simple, continuous rotation
- **Servo Motors**: Precise position control
- **Stepper Motors**: Discrete step movements

### 2. Hydraulic Actuators
- High force output
- Used in heavy-duty applications
- Common in industrial robots

### 3. Pneumatic Actuators
- Air-powered movement
- Fast response times
- Lightweight and safe

## Control Systems

Control systems ensure robots move accurately and smoothly:

### PID Control
The most common control algorithm:

```python title="pid_controller.py"
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.integral = 0
        self.previous_error = 0

    def compute(self, setpoint, measured_value, dt):
        """Compute control output"""
        error = setpoint - measured_value

        # Proportional term
        p_term = self.kp * error

        # Integral term
        self.integral += error * dt
        i_term = self.ki * self.integral

        # Derivative term
        derivative = (error - self.previous_error) / dt
        d_term = self.kd * derivative

        # Update previous error
        self.previous_error = error

        # Compute output
        output = p_term + i_term + d_term
        return output

# Example: Control robot arm position
controller = PIDController(kp=1.0, ki=0.1, kd=0.05)
```

## Motion Planning

Planning how robots move from point A to point B:

- **Path Planning**: Find collision-free paths
- **Trajectory Generation**: Create smooth motion profiles
- **Inverse Kinematics**: Calculate joint angles for desired positions

## Key Takeaways

- Actuators convert electrical signals into physical motion
- Control systems ensure precise and stable movement
- PID control is widely used for position and velocity control
- Motion planning enables complex, collision-free behaviors

---

## اردو ترجمہ (Urdu Translation)

# باب 3: حرکت اور کنٹرول

*تخمینی پڑھنے کا وقت: 7 منٹ*

## حرکت کا تعارف

حرکت وہ طریقہ ہے جس سے روبوٹس حرکت کرتے اور جسمانی دنیا کے ساتھ تعامل کرتے ہیں۔ ایکچویٹرز برقی توانائی کو مکینیکل حرکت میں تبدیل کرتے ہیں۔

## ایکچویٹرز کی اقسام

### 1. برقی موٹرز
- **DC موٹرز**: سادہ، مسلسل گردش
- **سرو موٹرز**: درست پوزیشن کنٹرول
- **سٹیپر موٹرز**: مجرد قدم کی حرکتیں

### 2. ہائیڈرولک ایکچویٹرز
- زیادہ قوت کی پیداوار
- بھاری ڈیوٹی ایپلیکیشنز میں استعمال
- صنعتی روبوٹس میں عام

### 3. نیومیٹک ایکچویٹرز
- ہوا سے چلنے والی حرکت
- تیز ردعمل کا وقت
- ہلکے اور محفوظ

## کنٹرول سسٹمز

کنٹرول سسٹمز اس بات کو یقینی بناتے ہیں کہ روبوٹس درست اور ہموار طریقے سے حرکت کریں۔

### PID کنٹرول
سب سے عام کنٹرول الگورتھم:

- **Proportional (تناسبی)**: موجودہ خرابی پر ردعمل
- **Integral (انٹیگرل)**: ماضی کی خرابیوں کو جمع کرتا ہے
- **Derivative (مشتق)**: مستقبل کی خرابی کی پیش گوئی کرتا ہے

## موشن پلاننگ

روبوٹس کو نقطہ A سے نقطہ B تک کیسے منتقل کرنا ہے اس کی منصوبہ بندی:

- **پاتھ پلاننگ**: تصادم سے پاک راستے تلاش کریں
- **ٹریجیکٹری جنریشن**: ہموار حرکت کے پروفائلز بنائیں
- **انورس کائنیمیٹکس**: مطلوبہ پوزیشنوں کے لیے جوائنٹ اینگلز کا حساب لگائیں

## اہم نکات

- ایکچویٹرز برقی سگنلز کو جسمانی حرکت میں تبدیل کرتے ہیں
- کنٹرول سسٹمز درست اور مستحکم حرکت کو یقینی بناتے ہیں
- PID کنٹرول پوزیشن اور رفتار کے کنٹرول کے لیے وسیع پیمانے پر استعمال ہوتا ہے
- موشن پلاننگ پیچیدہ، تصادم سے پاک رویوں کو ممکن بناتی ہے

---

**Next:** [Chapter 4: Learning & Intelligence](../chapter-04/index.md) →
