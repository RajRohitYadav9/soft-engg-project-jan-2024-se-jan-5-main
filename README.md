Software Engineering Project for January 2024 Term

**Problem Statement:**

Ticket System Integration with Discourse and Webhooks



There are many software solutions that work on top of existing applications and seamlessly integrate with them. Such an attempt will benefit from the good features of both, and prevent re-inventing the wheel by using modules which already exist. In the software engineering project this term, you will be building on top of an existing application which students built in a previous term of this course.



In a previous term of the course, the software engineering project assigned to students was to create an Online support ticket system for the IITM BS degree program. Here is the problem statement:



The support team at the IITM BS degree program often gets overwhelmed with emails from students regarding queries and concerns. Your task is to create an online support ticketing system for the IITM BS degree program. Students can create a support ticket for a particular concern or query. Before they create a ticket, the system should also show a list of similar tickets, and allow users to like or +1 an already existing support ticket, so that duplicates are not created. This way popular concerns or queries can be prioritised by the support team.



After the support team addresses the concern, they can mark the ticket as resolved, and an appropriate notification should be sent to concerned users.



Another important feature of the ticketing system is dynamic FAQ updation. Many student concerns can be FAQs which will be useful for future students. If appropriate, the support query and response should be added to the FAQ section by support admins, and appropriately categorised, so that an updated FAQ will be readily available to students. The platform should allow users to enroll as students, support staff and admins.



Apart from these standard requirements, you can also think of other features which can add value to users.



Based on this problem statement, students designed software solutions. We provide a sample of them below



1. Group 1 - Project 

2. Group 2 - Project

3. Group 3 - Project

4. Group 4 - Project



Link: https://drive.google.com/drive/folders/10B7-rmdvu1peTyKTber9Ys5wc_KXA6pO?usp=sharing

Assume that the IITM BS team decides to use one of the solution, but wants to integrate the same to the existing ecosystem that their team uses in the following ways:



Discourse Integration: In addition to the creation and listing of tickets, your system should also have the provision to create a Discourse thread for each ticket. This will involve integrating the Discourse system with the IITM BS ticketing system. You can think of different rules and configurations to create/edit/modify Discourse threads (for example - the thread can initially be private, but then can be converted to a public topic by moderators (link)). You can also think of additional features like notifications when a thread which you created has received a reply, like etc.
The Discourse API docs has an extensive set of APIs you can go through to think of what all features are possible to integrate with the ticketing system.


Webhooks Integration: Certain tickets can be high priority and need to be addressed immediately. In such cases, the system has to integrate with webhooks to notify High Priority and Urgent tickets into GChat. This can then be used by higher authorities for handling escalations (https://developers.google.com/chat/how-tos/webhooks)



For this project, you are required to Implement a prototype solution that will ensure integration and demonstrate the capabilities using a locally hosted system. All the software applications discussed in this problem are either open source or have knowledge bases that will allow implementation to happen within a 3 month period.


**Project Milestones:**

DEADLINES:  

Milestone 1: Deadline by the end of Week 3 [23rd February 2024]
Milestone 2: Deadline by the end of Week 5  [29th February 2024]
Milestone 3: Deadline by the end of Week 6  [5th March 2024]
Milestone 4: Deadline by the end of Week 8 [15th March 2024]
Milestone 5: Deadline by the end of Week 10 [29th March 2024]
Milestone 6: Deadline by end of Week 12 [17th April 2024]

***1. Milestone 1- Identify User Requirements:***

Identify users of the application - primary, secondary and tertiary users.

Write user stories for the requirements, based on the SMART guidelines discussed in the lectures (You are not required to write user stories for existing functionalities; instead, you have to write them for the features and integrations you want to implement in the existing system)

The user stories should be in the following format:

As a [type of user],

I want [an action],

So that [a benefit/value]





***2. Milestone 2- User Interfaces:*** 

Create a storyboard for the application - it can be a ppt or even a video. Embed the ppt/video in the pdf submission of this week.

Take each user story and create low-fidelity wireframes

Apply usability design guidelines and heuristics discussed in lectures to come up with the wireframes.



***3. Milestone 3- Scheduling and Design:***  

Project Schedule - come up with a schedule of your overall project based on the user stories created in the previous milestones. 
Create a schedule for your sprints and iterations, timings of your scrum meetings etc. Trello board, Gantt chart - specifying your tasks and contributions.

Project Scheduling Tools - which tools are you using? E.g. Pivotal Tracker, Jira 

Design of Components - Describe different components of your system based on the user stories created in the previous milestones.

Software Design - Basic class diagrams of your proposed system.

Details/Minutes of a scrum meetings

Milestone 3 Pdf Report.





***4. Milestone 4 - API Integrations:***  

For each user story, use appropriate API endpoints.

Description of API endpoints. [As per the problem statement]

Submission should be as a yaml file.





***5. Milestone 5 - Test cases, test suite of the project:*** 

For each API endpoint, design extensive test cases. Test cases should be in the following format:

		[ API being tested,

		Inputs,

		Expected output,

		Actual Output,

		Result- Success/Fail ]





***6. Milestone 6 - Final Submission:*** 

Week-12 is completely focused on the project, and no new course content is released this week.

Complete implementation along with a working prototype.

Final project report(consistent with intermediate milestone documents).

Detailed report on work done from Milestone 1 through Milestone 5.

Implementation details of your project

Technologies and tools used.

Where is your application hosted(if hosted)? (hosting is not compulsory)

And instructions to run your application.

A section describing code review, issue reporting and tracking using screenshots.

Recorded presentation of the working model of your system.


Components evaluated in final Project Evaluation:

The overall design of the project.

Teamwork that includes code review, issue reporting and tracking etc.

Efficient coding practices.

Consistent design through different milestones.
