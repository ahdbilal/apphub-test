import 'package:flutter/material.dart';

void main() {
  runApp(TabBarDemo());
}

class TabBarDemo extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: DefaultTabController(
        length: 4,
        child: Scaffold(
          appBar: AppBar(
            bottom: TabBar(
              tabs: [
                Tab(icon: Icon(Icons.all_inclusive)),
                Tab(icon: Icon(Icons.build )),
                Tab(icon: Icon(Icons.zoom_out_map)),
                Tab(icon: Icon(Icons.bug_report  ))
              ],
            ),
            backgroundColor: const Color(0xFFC51162),
            title: Text('Visual Studio App Center'),
          ),
          body: TabBarView(
            children: [
              Center(
                child: Container(
                  margin: const EdgeInsets.symmetric(vertical: 60.0,horizontal: 20.0),
                    child: Column(
                      children: <Widget>[
                          SizedBox(height: 40),
                          Expanded(
                            child: FittedBox(
                              fit: BoxFit.contain, // otherwise the logo will be tiny
                              child: const Image(
                                image: AssetImage('assets/appcenter.png'),
                              ),
                            ),
                          ),
                          SizedBox(height: 40),
                          Flexible(
                            child: new Text(
                              "Continuously build, test, release, and monitor apps for every platform.",
                              textAlign: TextAlign.center,
                              style: TextStyle(fontSize: 20.0),
                            )
                          ),
                      ],
                    ),
                    alignment: Alignment(0.0, -1.0),
                ),
              ),
              Center(
                child: Container(
                  margin: const EdgeInsets.symmetric(vertical: 60.0,horizontal: 20.0),
                    child: Column(
                      children: <Widget>[
                        Text(
                          'Build',
                          textAlign: TextAlign.center,
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 20),
                        Expanded(
                          child: FittedBox(
                            fit: BoxFit.contain, // otherwise the logo will be tiny
                            child: const Image(
                              image: AssetImage('assets/build.png'),
                            ),
                          ),
                        ),
                        SizedBox(height: 10),
                        Flexible(
                          child: new Text(
                            "The App Center Build service helps you build Android, iOS, macOS, and UWP apps using a secure cloud infrastructure. Connect to your repo in App Center and start building your app in the cloud on every commit. With Build you can forget about configuring build servers locally, complicated configurations, and code that builds on a coworker's machine but not yours.",
                            textAlign: TextAlign.center,
                            style: TextStyle(fontSize: 14.0),
                          )
                        ),
                      ],
                    ),
                    alignment: Alignment(0.0, -1.0),
                ),
              ),
              Center(
                child: Container(
                  margin: const EdgeInsets.symmetric(vertical: 60.0,horizontal: 20.0),
                    child: Column(
                      children: <Widget>[
                        Text(
                          'Distribute',
                          textAlign: TextAlign.center,
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 10),
                        Expanded(
                          child: FittedBox(
                            fit: BoxFit.contain, // otherwise the logo will be tiny
                            child: const Image(
                              image: AssetImage('assets/distribute.png'),
                            ),
                          ),
                        ),
                        SizedBox(height: 20),
                        Flexible(
                          child: new Text(
                            "App Center Distribute is a tool for developers to quickly release builds to end user devices. Distribute supports Android, iOS, macOS, UWP, WPF and WinForms apps, allowing you to manage app distribution across multiple platforms all in one place. With a complete install portal experience, Distribute is not only a powerful solution for beta app tester distribution but also a convenient alternative to distribution through the public app stores.",
                            textAlign: TextAlign.center,
                            style: TextStyle(fontSize: 14.0),
                          )
                        ),
                      ],
                    ),
                    alignment: Alignment(0.0, -1.0),
                ),
              ),
              Center(
                child: Container(
                  margin: const EdgeInsets.symmetric(vertical: 60.0,horizontal: 20.0),
                    child: Column(
                      children: <Widget>[
                        Text(
                          'Diagnostics',
                          textAlign: TextAlign.center,
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 20),
                        Expanded(
                          child: FittedBox(
                            fit: BoxFit.contain, 
                            child: const Image(
                              image: AssetImage('assets/diagnostics.png'),
                            ),
                          ),
                        ),
                        SizedBox(height: 10),
                        Flexible(
                          child: new Text(
                            "App Center Diagnostics is a cloud service that helps developers monitor the health of an application, delivering the data needed to understand what happens when an app fails during testing or in the wild. The App Center Diagnostics SDK collects information about crashes and uploads them to the App Center portal for analysis - eliminating the guesswork about what really happened in the app when it failed.",
                            textAlign: TextAlign.center,
                            style: TextStyle(fontSize: 14.0),
                          )
                        ),
                      ],
                    ),
                    alignment: Alignment(0.0, -1.0),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
