# 0. Experiment Overview: Free Trial Screener

At the time of this experiment, Udacity courses currently have two options on the course overview page: "start free trial", and "access course materials". If the student clicks "start free trial", they will be asked to enter their credit card information, and then they will be enrolled in a free trial for the paid version of the course. After 14 days, they will automatically be charged unless they cancel first. If the student clicks "access course materials", they will be able to view the videos and take the quizzes for free, but they will not receive coaching support or a verified certificate, and they will not submit their final project for feedback.  

In the experiment, Udacity tested a change where if the student clicked "start free trial", they were asked how much time they had available to devote to the course. If the student indicated 5 or more hours per week, they would be taken through the checkout process as usual. If they indicated fewer than 5 hours per week, a message would appear indicating that Udacity courses usually require a greater time commitment for successful completion, and suggesting that the student might like to access the course materials for free. At this point, the student would have the option to continue enrolling in the free trial, or access the course materials for free instead. This [screenshot](https://drive.google.com/file/d/0ByAfiG8HpNUMakVrS0s4cGN2TjQ/view) shows what the experiment looks like. Some [baseline](https://docs.google.com/spreadsheets/d/1MYNUtC47Pg8hdoCjOXaHqF-thheGpUshrFA21BAJnNc/edit#gid=0) values were provided in this spreadsheet.

<img src="img/ScreenShot.jpeg"></img>

The hypothesis was that this might set clearer expectations for students upfront, thus reducing the number of frustrated students who left the free trial because they didn't have enough time—without significantly reducing the number of students to continue past the free trial and eventually complete the course. If this hypothesis held true, Udacity could improve the overall student experience and improve coaches' capacity to support students who are likely to complete the course.  

The unit of diversion is a cookie, although if the student enrolls in the free trial, they are tracked by user-id from that point forward. The same user-id cannot enroll in the free trial twice. For users that do not enroll, their user-id is not tracked in the experiment, even if they were signed in when they visited the course overview page.  

# 1. Metric Choice

## 1.1 Instruction

Which of the following metrics would you choose to measure for this experiment and why? For each metric you choose, indicate whether you would use it as an invariant metric or an evaluation metric. The practical significance boundary for each metric, that is, the difference that would have to be observed before that was a meaningful change for the business, is given in parentheses. All practical significance boundaries are given as absolute changes.
Any place "unique cookies" are mentioned, the uniqueness is determined by day. (That is, the same cookie visiting on different days would be counted twice.) User-ids are automatically unique since the site does not allow the same user-id to enroll twice.   

Any place "unique cookies" are mentioned, the uniqueness is determined by day. (That is, the same cookie visiting on different days would be counted twice.) User-ids are automatically unique since the site does not allow the same user-id to enroll twice.  

+ _Number of cookies_: That is, number of unique cookies to view the course overview page. **(dmin=3000)**
+ _Number of user-ids_: That is, number of users who enroll in the free trial. **(dmin=50)**
+ _Number of clicks_: That is, number of unique cookies to click the "Start free trial" button (which happens before the free trial screener is trigger). **(dmin=240)**
+ _Click-through-probability_: That is, number of unique cookies to click the "Start free trial" button divided by number of unique cookies to view the course overview page. **(dmin=0.01)**
+ _Gross conversion_: That is, number of user-ids to complete checkout and enroll in the free trial divided by number of unique cookies to click the "Start free trial" button. **(dmin= 0.01)**
+ _Retention_: That is, number of user-ids to remain enrolled past the 14-day boundary (and thus make at least one payment) divided by number of user-ids to complete checkout. **(dmin=0.01)**
+ _Net conversion_: That is, number of user-ids to remain enrolled past the 14-day boundary (and thus make at least one payment) divided by the number of unique cookies to click the "Start free trial" button. **(dmin= 0.0075)**
  
You should also decide now what results you will be looking for in order to launch the experiment. Would a change in any one of your evaluation metrics be sufficient? Would you want to see multiple metrics all move or not move at the same time in order to launch? This decision will inform your choices while designing the experiment.  

## 1.2 Answer

Here is the overall view of user path:

<img src="img/User FLow.jpeg"></img>

Base on the flow chart above, it is clear that we should use the following **invariant variables** and **evaluation metrics**. 

### 1.2.1 Invariant Variables

+ **Number of cookies**: this metric should not be affected by the experiment we run, since the experiment will be running between Free trial stage and Enrollment stage, therefore we should keep the variables before the enrollment stage as the same as possible for control and experiment group.
+ **Number of clicks**: this metric also should not be affected by the experiment, the reason is the same.
+ **Click-through-probability**: this metric also should not be affected by the experiment, the reason is the same.

### 1.2.2 Evaluation metrics

+ **Gross conversion**: this metric can be affected since the students in the experiment group will be asked about how much time they can devote in this course, if the answer is less than 5 hours, they will be suggested learning from free material rather than starting this free trial, as a result, the enrollment page will not be shown and the nominator of this metric will be affected.
+ **Retention**: this metric can also be affected because of the same reason mentioned above, to be specific, both the numerator and denominator should have difference between the control group and experiment group. 
+ **Net conversion**: this metric can also be affected because of the same reason mentioned above, to be specific, the numerator will be affected in the experiment group.  

To summarize, the goals of this experiment are:

1. Number of the payments should not decrease.
2. Number of students who do not have enough time should decrease.

By having the goals above, our Evaluation metrics should:

1. Gross conversion: decrease
2. Retention: increase
3. Net conversion: remain the same or increase

### 1.2.3 Standard Deviation of Evaluation metrics

Baseline values are as follows:

|Description|Number|
|---|---:|
|Unique cookies to view course overview page per day|    40000|
|Unique cookies to click "Start free trial" per day| 3200|
|Enrollments per day|    660|
|Click-through-probability on "Start free trial"|    0.08|
|Probability of enrolling, given click|  0.20625|
|Probability of payment, given enroll|   0.53|
|Probability of payment, given click| 0.1093125|

For each metric you selected as an evaluation metric, make an analytics estimate of its standard deviation, given a sample size of 5000 cookies visiting the course overview page

1. Gross conversion (binorm std)

Number of unique cookies clicking the "Start free trail" button = 5000 * 0.08 = 400

Std of Gross conversion = Sqrt(0.20625 * (1 - 0.20625) / 400) = 0.0202

2. Retention
Number of unique cookies complete the check out = 400 * 0.20625 = 82.5  

Std of Retension = Sqrt(0.53 * (1-0.53) / 82.5) = 0.0549

3. Net conversion 
 
Std of Net conversion = Sqrt(0.1093125 * (1 - 0.1093125) / 400) = 0.0156

# 2. Size

## 2.1 Choosing Number of Samples given Power

Using the analytic estimates of variance, how many pageviews total (across both groups) would you need to collect to adequately power the experiment? Use an alpha of 0.05 and a beta of 0.2. Make sure you have enough power for each metric.  

Here is an online calculator for sample size: [A/B Testing Tools](https://www.evanmiller.org/ab-testing/sample-size.html) 

1. Gross conversion

<img src="img/Sample Size_Gross conversion.jpeg"></img>

2. Retention

<img src="img/Sample Size_Retention.jpeg"></img>

3. Net conversion

<img src="img/Sample Size_Net conversion.jpeg"></img>

Since the sample size here is not the number of pageviews, so we need to calculate the needed pageviews for each metric

For Gross conversion: Pageview needed = 25835 / (3200 / 40000) * 2 = 645875  
For Retention: Pageview needed = 39115 / (660 / 40000) * 2 = 4741212  
For Net conversion: Pageview needed = 27413 / (3200 / 40000) * 2 = 685325

In summary:

|Metrics|Sample Size|Pageview Needed|
|---|---:|---:|
|Gross conversion|25,835|645,875|
|Retention|39,115|4,741,212|
|Net conversion|27,413|685,325|

Therefore, the number of pageviews is 4,741,212. But in terms of practical view, if this experiment needs 4,741,212 pageviews, which means 4,741,212 / 40,000 = 119 days, it is too long for doing an experiment, therefore after this step, we will not use Retention as one of our Evaluation metrics.

So the total pageviews we are going to need are 685,325. 

## 2.2 Choosing Duration vs. Exposure

What percentage of Udacity's traffic would you divert to this experiment (assuming there were no other experiments you wanted to run simultaneously)? Is the change risky enough that you wouldn't want to run on all traffic?  

Given the percentage you chose, how long would the experiment take to run, using the analytic estimates of variance? If the answer is longer than a few weeks, then this is unreasonably long, and you should reconsider an earlier decision.  

I would use 80% of the total traffic in this experiment and it will take 22 days to complete this experiment. 

# 3. Analysis

The data for you to analyze is [here](https://docs.google.com/spreadsheets/d/1Mu5u9GrybDdska-ljPXyBjTpdZIUev_6i7t4LRDfXM8/edit#gid=0). This data contains the raw information needed to compute the above metrics, broken down day by day. Note that there are two sheets within the spreadsheet - one for the experiment group, and one for the control group.  

The meaning of each column is:
+ Pageviews: Number of unique cookies to view the course overview page that day.
+ Clicks: Number of unique cookies to click the course overview page that day.
+ Enrollments: Number of user-ids to enroll in the free trial that day.
+ Payments: Number of user-ids who enrolled on that day to remain enrolled for 14 days and thus make a payment. (Note that the date for this column is the start date, that is, the date of enrollment, rather than the date of the payment. The payment happened 14 days later. Because of this, the enrollments and payments are tracked for 14 fewer days than the other columns.)

## 3.1 Sanity Checks

Start by checking whether your invariant metrics are equivalent between the two groups. If the invariant metric is a simple count that should be randomly split between the 2 groups, you can use a binomial test as demonstrated in Lesson 5. Otherwise, you will need to construct a confidence interval for a difference in proportions using a similar strategy as in Lesson 1, then check whether the difference between group values falls within that confidence level. 

||Clicks|Pageviews|
|---|---:|---:|
|Control Group|28,378|345,543|
|Experiment Group|28,325|344,660|

**Number of cookies**

Our assumption here is when we were doing the experiment, the probability for a specific cookie signed to the control group or experiment group is the same, which is 50%, so here p = 0.5. 

Standard Error of cookies = Sqrt(0.5 * (1 - 0.5) / (345,543 + 344,660)) = 0.0006018  

Margin of Standard Error = Standard Error of cookies * 1.96 = 0.00117953. 

Therefore, the Confidence Interval is [0.4988, 0.5011], since p hat (345,543 / (345,543 + 344,660) = 0.5005) is in this interval, we can say Number of cookies passes the Sanity Check.  

**Number of clicks**

Here we have the same assumption, p = 0.5  

Standard Error of clicks = Sqrt(0.5 * (1 - 0.5) / (28,378 + 28,325)) = 0.0021  

Margin of Standard Error = 0.0021 * 1.96 = 0.004116  

Therefore, the Confidence Interval is [0.4959, 0.5041], since p hat (28,378 / (28,378 + 28,325) = 0.5005) is in this interval, we can say Number of clicks passes the Sanity Check.  

**Click-through-probability** 

p_pool = (28,378 + 28,325) / (345,543 + 344,660) = 0.0822  

Standard Error of Click-through-probability = Sqrt(0.0822 * (1 - 0.0822) * (1 / 345,543 + 1 / 344,660)) = 0.000661229  

Margin of Standard Error = 0.0013  

Therefore, the Confidence Interval is [-0.0013, 0.0013], since d hat (0.082182441 - 0.082125814 = 5.66271E-05) is in this interval, we can say Click-through-probability passes the Sanity Check.  

## 3.2 Check for Practical and Statistical Significance

Next, for your evaluation metrics, calculate a confidence interval for the difference between the experiment and control groups, and check whether each metric is statistically and/or practical significance. A metric is statistically significant if the confidence interval does not include 0 (that is, you can be confident there was a change), and it is practically significant if the confidence interval does not include the practical significance boundary (that is, you can be confident there is a change that matters to the business.)  

||Clicks|Enrollments|Payments|
|---|---:|---:|---:|
|Control Group|17,293|3,785|2,033|
|Experiment Group|17,260|3,423|1,945|

**Gross conversion**

p_pool = Sqrt((3,785 + 3,423) / (17,293 + 17,260)) = 0.2086  

Standard Error of Gross conversion = Sqrt(0.2086 * (1 - 0.2086) * (1 / 17,293 + 1 / 17,260)) = 0.0044  

Margin of Standard Error = 0.0086  

Difference = 3,423 / 17,260 - 3,785 / 17,293 = -0.0206  

Therefore, the Confidence Interval is [-0.0292, -0.012], since 0 is not in this interval and -0.1 is not in this interval, we can say that the change of Gross conversion is Statistical significance and Practical significance

**Net conversion**

p_pool = Sqrt((2,033 + 1,945) / (17,293 + 17,260)) = 0.1151  

Standard Error of Net conversion = Sqrt(0.1151 * (1 - 0.1151) * (1 / 17,293 + 1 / 17,260)) = 0.0034  

Margin of Standard Error = 0.0067  

Difference = 1,945 / 17,260 - 2,033 / 17,293 = -0.0049  

Therefore, the Confidence Interval is [-0.0116, 0.0018], since 0 is in this interval and -0.1 is in this interval, we can say that the change of Gross conversion is not Statistical significance and not Practical significance. 


## 3.3 Run Sign Tests

||Positive Change|Count|
|---|---:|---:|
|Gross conversion|4|23|
|Net conversion|10|23|

As shown in this [calculator](https://www.graphpad.com/quickcalcs/binomial1.cfm), the p-value for Gross conversion is 0.0026, and the p-value for Net conversion is 0.6776, meaning Gross conversion passes the sign test while Net conversion does not pass the sign test.

## 3.4 Make a Recommendation

As the analysis, I do not recommend launch this feature since the negative effect is larger than the positive effect, although the gross conversion rate decreases significantly, the net conversion does not show a significant positive change, which may cause a huge financial loss in the future. 

# References

+ [Project Instruction](https://docs.google.com/document/u/1/d/1aCquhIqsUApgsxQ8-SQBAigFDcfWVVohLEXcV6jWbdI/pub?embedded=True)
+ [Baseline Values](https://docs.google.com/spreadsheets/d/1MYNUtC47Pg8hdoCjOXaHqF-thheGpUshrFA21BAJnNc/edit#gid=0)
+ [A/B Testing Tools](https://www.evanmiller.org/ab-testing/sample-size.html)
+ [Experiment Data](https://docs.google.com/spreadsheets/d/1Mu5u9GrybDdska-ljPXyBjTpdZIUev_6i7t4LRDfXM8/edit#gid=0)
+ [Sign Test](https://www.graphpad.com/quickcalcs/binomial1.cfm) 


