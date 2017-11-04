# Virtual Assistant

## State of the Art and Preliminary Work

Expert systems are becoming popular in recent years because they are very helpful in
solving problems related to decision making in different fields, especially in healthcare and
management. An expert system is a software that uses knowledge of an expert in the field
of interest. Basically they act like experts: collect data, analyse it and then produce
algorithm of actions or recommendations for an action. Sometimes they can be autonomous
and directly connected to actuators. As a result, expert systems can act or change the
environment based on their own recommendations. This paper is a continuation and
upgrade of the expert system called “Virtual Assistant” developed by a team from the
Middlesex University in the Sunny Hill House.

Virtual Assistant of the Middlesex University developed by Kenzhegali Nurgaliyev,
Dario Di Mauro and others in 2016 is a system that assists people in their Activities of
Daily Life (ADL). The system uses Graphical User Interface with text based dialogue
window; speech recognition and text to speech generating software based voice dialogue
window. Virtual Assistant uses pre-defined preferences based on age of the user profile
with differentiated priorities of the needs including health, entertainment, security and
energy consumption of the devices. Virtual Assistant passed the validation tests done by
the developers and showed acceptable results in conflict resolution. However, there is an
issue about two identical profile users with conflicting activities; for example, user “1”
asks the system to turn on the light while user “2” with the same priority level as the user
“1” asked the system to turn the light off. The aim of this research is to create a dialogue
based conflict resolution system that takes into account pre-defined preferences and adapts
to the new information learned from dialogue with users.

## Research Question and Methodology

The aim of the research is to create a voice based dialogue manager for multi-users
with identical priority that allows controlling actuators inside the Sunny Hill House in
conflict situations. Conflict Resolution sub-system will communicate with different users
to collect the data about reasoning behind the actions they want to be done by the system.
For example, if two identical users want conflicted actions to be done they will
communicate with system to give reasons to act in the way they want. After that, the system
will make a decision based on the new information gained from users and will give
recommendations till the conflict will be eliminated. An example of that situation is
described in the scenario template in the end of the proposal.

The system has the architecture of module-based system where any of the module can
be used as an autonomous system. Firstly, there is speech recognition module that uses
well-developed speech recognition API with high efficiency, for example Yandex
SpeechKit, to recognize the speech and semantically analyze the text. The second module
is actuators control and monitor module. Thirdly, there is core of the system that is
Dialogue Manager with unified input-output structure or API. API makes it possible to use
and integrate Dialogue Manager as a module in other projects in future. In addition, there
is speech synthesizer of the system. To evaluate the system, several test scenarios with
randomized-blind user feedback to the system will be created.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

## Bibliography concerning the state of the art and the research objectives

B. S. Hasler, P. Tuchman and D. Friedman, “Virtual research assistants: Replacing human
interviewers by automated avatars in virtual worlds”, in Computers in Human Behavior, v.29
n.4, p.1608-1616, July, 2013.
K. Mase, “Aspects of Interface Agents: Avatar, Assistant and Actor”, in Proceedings of the
IJCAI'97 Workshop on Animated Interface Agents, pp. 33-37.
K. Nurgaliyev, D. D. Mauro, N. Khan and J. C. Augusto, “Improved Multi-user Interaction in
a Smart Environment Through a Preference-Based Conflict Resolution Virtual Assistant”.