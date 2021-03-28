The goal of **Adelego** is to protect and support dependent people, caregivers and people living by themselves. 

### The problem
A person becomes **dependent** because of their age, a disability and / or an illness and a **caregiver** is a person who helps dependent people in their daily life. When an accident happens to dependent people or people living by themselves, their health can be severely impacted. We are observing that the proportion of people who live by themselves is also on the rise and that countries across Europe and the Americas are aging leading to an increase in the number of dependent people and consequently, caregivers.

It is estimated that today, about 1 in 5 people is a caregiver in Europe and North America and statistics indicate that this number is going to increase for the next few decades. Unfortunately, this situation will not be sustainable economically very soon which is why we want to develop solutions that are durable, simple and economical and that can help as many of these people as possible.

### Our project
We are turning to the use of connected objects and the implementation of digital applications to develop a **local home surveillance system** that :
(1) allows dependent people and people who are living by themselves to live safer and longer in their own home
(2) provides relief for their caregivers and loved ones.

Because each situation is unique and changes over time, our approach is to create a **platform** that will provide a variety of tools allowing these people to pick tools based on their needs.
Each tool will contain one or several functionalities, record and analyze data locally and send an alert (by phone or email) to a trusted third party when an unusual activity happens, such as a fall.

### First prototype
We are currently building a first prototype consisting of a detector connected to a Raspberry Pi 4 on which we installed Jeedom.

*Raspberry Pi 4 and the antenna*

<img src="assets/images/IMG_3160.jpg"	title="Raspberry Pi 4 and the antenna" width="300" height="400" /> 

*Multisensor 6 detector*

<img src="assets/images/IMG_3163.jpg"	title="Multisensor 6 detector" width="300" height="400" /> 

The detector we  are using is Multisensor 6 from [Aeotec](https://aeotec.com/z-wave-sensor/). This detector can sense humidity, temperature, presence, UV, brightness and vibration. It uses the Z-wave protocol to communicate to its antenna ([Z-stick Gen 5+](https://aeotec.com/z-wave-usb-stick/)) that is hooked up to the Raspberry Pi.

[Jeedom](https://www.jeedom.com/en/) is an open-source software that is designed to create a personalized home automation system. We are currently using Jeedom to collect and export our data as CSV files.

The detector has been placed at the entrance of our kitchen since December 1st 2020 and has been recording data continuously.

The appropriate data analysis is essential to detect any unusual activity. Our current strategy is to use the Python library, *pandas*, to analyze the data. For example, we want to determine when someone enters the kitchen for the first time of the day, get an average and standard deviation. This will create a history of usual activity. If this time starts changing, then an alert is sent to a person of our choice. 

### Let's work together
If you want to develop this project with us or have ideas/suggestions, feel free to contact me on GitHub or <adele.jmb@gmail.com>.

We also created a GitHub page (in french) with more information on the project and our vision [here](https://mbonnemaison.github.io/adelego/).
*We thank the Boston Python group for allowing us to use their GitHub page as a model for our GitHub page: [about.bostonpython.com](https://about.bostonpython.com)*
