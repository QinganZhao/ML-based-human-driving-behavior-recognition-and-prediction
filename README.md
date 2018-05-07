<div align=center>
 
# Machine Learning Based Human Driving Behavior Recognition and Prediction

[**Hengbo Ma**](https://hengboma.github.io), [**Franklin Zhao**](http://franklinzhao.top), **Jessica Leu, and Yujun Zou**

May 2018

<div align=left>

Prediction and recognition in complex situation have significant
influence on the overall performance of autonomous driving systems. Many
works focusing on single driver’s behavior have been done. However,
modeling multi-driver interaction, which is a more general case, is
harder. In our project, we first divide human driving behavior into a
hierarchical model which contains decision-making phase and maneuver
phase. Next, we use classifiers to find the drivers’ high-level
intention, i.e., decision making, and then, we use Gaussian Mixture
Models to capture different human driving behavior given their high
level decisions. Last, base on the assumption that decisions in training
data are unknown to us, we use a variational autoencoder to learn the
representation of different driver behavior models in latent space and
make prediction accordingly. A simulation data set from ramp-merging
scenario is used to verify each models.
