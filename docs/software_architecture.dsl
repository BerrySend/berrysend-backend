workspace "BerrySend" "App for planning export routes of berries" {

    !identifiers hierarchical

    //
    // CONTEXT DIAGRAM
    //
    model {

        //
        // TARGET SEGMENTS
        //
        exporter = person "Exporter" "User that will use the BerrySend app to plan export routes"

        //
        // SOFTWARE
        //
        berrySend = softwareSystem "BerrySend" "Service to plan and optimize export routes" "App" {

            //
            // CONTAINER DIAGRAM
            //
            webApplication = container "Web Application" "Delivers the static content and the BerrySend single page application" "" "" {

            }

            singlePageApplication = container "Client-Side Application" "Provides all of the BerrySend functionality to the user browser." "" "Web" {
                technology "JavaScript, Vue.JS and TailwindCSS"

                //
                // COMPONENTS DIAGRAM - Client-Side App
                //

                appComponent = component "AppComponent" "Displays and contains the main UI components."

                //
                // BOUNDED CONTEXT AUTHENTICATION
                //

                // PAGES
                loginPage = component "LoginPage" "Page for login activities." {
                    technology "Vue.js Component"
                }
                registerPage = component "RegisterPage" "Page for registratation activities." {
                    technology "Vue.js Component"
                }

                // COMPONENTS
                loginFormComponent = component "LoginFormComponent" "Handles user authentication." {
                    technology "Vue.js Component"
                }
                registerFormComponent = component "RegisterFormComponent" "User registration form." {
                    technology "Vue.js Component"
                }
                authLayout = component "AuthLayout" "Layout wrapper for authentication pages (login and register)" {
                    technology "Vue.js Component"
                }

                // SERVICES
                authService = component "AuthService" "Manages authentication logic and make requests to the API." {
                    technology "JavaScript Component"
                }
                userService = component "UserService" "Manages user logic and make requests to the API." {
                    technology "JavaScript Component"
                }

                //
                // BOUNDED CONTEXT PORT MANAGEMENT
                //

                // PAGES
                portPage = component "PortPage" "Page for obtaining details of current ports." {
                    technology "Vue.js Component"
                }

                // COMPONENTS
                portCardComponent = component "PortCardComponent" "Sets the info of a port in a single organized card." {
                    technology "Vue.js Component"
                }

                // SERVICES
                portService = component "PortService" "Manages port logic and make requests to the API." {
                    technology "JavaScript Component"
                }

                //
                // BOUNDED CONTEXT ROUTE OPTIMIZATION
                //

                // PAGES
                optimizationPage = component "OptimizationPage" "Central page for optimizing routes by configuring parameters" {
                    technology "Vue.js Component"
                }

                // COMPONENTS
                algorithmCardComponent = component "AlgorithmCardComponent" "Card for describing details of used algorithms in the optimization" {
                    technology "Vue.js Component"
                }

                // SERVICES
                optimizationService = component "OptimizationService" "Manages optimization logic and make requests to the API for usage of algorithms" {
                    technology "JavaScript Component"
                }

                //
                // BOUNDED CONTEXT EXPORT MANAGEMENT
                //

                // PAGES
                visualizationPage = component "VisualizationPage" "Page for see the map with the optimized routes and info about the planned export" {
                    technology "Vue.js Component"
                }

                // COMPONENTS
                networkGraphComponent = component "NetworkGraphComponent" "Displays an interactive network graph with ports, connections and routes" {
                    technology "Vue.js Component"
                }

                // SERVICES
                graphService = component "GraphService" "Manages graph generation logic from the API" {
                    technology "JavaScript Component"
                }

                //
                // BOUNDED CONTEXT PROFILE MANAGEMENT
                //

                // PAGES
                profilePage = component "ProfileComponent" "Displays user profile data." {
                    technology "Vue.js Component"
                }
                editProfileComponent = component "EditProfileComponent" "Edits user profile details." {
                    technology "Vue.js Component"
                }

                // SERVICES
                profileService = component "ProfileService" "Fetches/updates profile data." {
                    technology "JavaScript Component"
                }

                //
                // ADITIONAL CONFIG
                //
                languageSwitcherComponent = component "LanguageSwitcherComponent" "Allows user to switch app language." {
                    technology "Vue.js Component"
                }

                navComponent = component "NavComponent" "Component for navigation through the app" {
                    technology "Vue.js Component"
                }
             }

            apiPlatform = container "Server-Side Application" "Provides BerrySend functionality via JSON/HTTP through the API." "" "API" {
                technology "Python and FastAPI"

                //
                // COMPONENTS DIAGRAM - API Platform
                //
                portManagement = component "Port Management Bounded Context" "Manages the creation and updating of ports and its connections from online CSV files" "" "Component" {
                    technology "Python Component"
                }

                routeOptimization = component "Route Optimization Bounded Context" "Manages and uses complex algorithms to optimize various factors about routes for exports" "" "Component" {
                    technology "Python Component"
                }

                exportManagement = component "Export Management Bounded Context" "Manages the planning of blue berry exports" "" "Component" {
                    technology "Python Component"
                }

                authentication = component "IAM Bounded Context" "Manages authentication, security and access control" "" "Component" {
                    technology "Python Component"
                }

                profileManagement = component "Profile Management Bounded Context" "Manages user profile information" "" "Component" {
                    technology "Python Component"
                }

                sharedKernel = component "Shared Kernel" "Provide shared utilities and abstractions" "" "Component" {
                    technology "Python Component"
                }
            }

            db = container "Relational Database" "Stores users information, planned routes and exports. " "" "BD" {
                technology "MySQL"
            }
        }

        //
        // EXTERNAL SYSTEMS
        //
        googleMaps = softwareSystem "Google Maps" "Service for using real-time maps" "ExternalSoftwareSystem"

        // -----------------------------------------------------------------------------------------------------------

        //
        // RELATIONS
        //

        //
        // CONTEXT DIAGRAM
        //

        exporter -> berrySend.webApplication "Uses"

        berrySend -> googleMaps "Uses to generate maps of routes"

        //
        // CONTAINER DIAGRAM
        //

        berrySend.webApplication -> berrySend.singlePageApplication "Delivers"

        berrySend.singlePageApplication -> googleMaps "Uses to generate maps of routes"
        berrySend.singlePageApplication -> berrySend.apiPlatform "Make requests via [HTTP/JSON]"

        berrySend.apiPlatform -> berrySend.db "Reads from and writes to"

        //
        // COMPONENT DIAGRAM
        //

        //
        // Single-Page App
        //
        berrySend.webApplication -> berrySend.singlePageApplication.appComponent "Delivers"

        berrySend.singlePageApplication.appComponent -> berrySend.singlePageApplication.loginPage "Sends to"

        berrySend.singlePageApplication.loginPage -> berrySend.singlePageApplication.loginFormComponent "Uses"
        berrySend.singlePageApplication.loginPage -> berrySend.singlePageApplication.registerPage "If not has an account, sends to"
        berrySend.singlePageApplication.loginPage -> berrySend.singlePageApplication.navComponent "If correctly authenticated, sends to"
        berrySend.singlePageApplication.loginPage -> berrySend.singlePageApplication.authService "Uses"
        berrySend.singlePageApplication.loginPage -> berrySend.singlePageApplication.userService "Uses"
        berrySend.singlePageApplication.loginPage -> berrySend.singlePageApplication.authLayout "Uses"

        berrySend.singlePageApplication.registerPage -> berrySend.singlePageApplication.registerFormComponent "Uses"
        berrySend.singlePageApplication.registerPage -> berrySend.singlePageApplication.authService "Uses"
        berrySend.singlePageApplication.registerPage -> berrySend.singlePageApplication.authLayout "Uses"
        berrySend.singlePageApplication.registerPage -> berrySend.singlePageApplication.navComponent "If correctly created an account, sends to"

        berrySend.singlePageApplication.navComponent -> berrySend.singlePageApplication.languageSwitcherComponent "Uses"
        berrySend.singlePageApplication.navComponent -> berrySend.singlePageApplication.visualizationPage "Sends to"
        berrySend.singlePageApplication.navComponent -> berrySend.singlePageApplication.optimizationPage "Sends to"
        berrySend.singlePageApplication.navComponent -> berrySend.singlePageApplication.portPage "Sends to"
        berrySend.singlePageApplication.navComponent -> berrySend.singlePageApplication.profilePage "Sends to"

        berrySend.singlePageApplication.visualizationPage -> berrySend.singlePageApplication.networkGraphComponent "Uses"
        berrySend.singlePageApplication.visualizationPage -> berrySend.singlePageApplication.graphService "Uses"
        berrySend.singlePageApplication.visualizationPage -> googleMaps "Uses to generate maps of routes"

        berrySend.singlePageApplication.optimizationPage -> berrySend.singlePageApplication.algorithmCardComponent "Uses"
        berrySend.singlePageApplication.optimizationPage -> berrySend.singlePageApplication.optimizationService "Uses"

        berrySend.singlePageApplication.portPage -> berrySend.singlePageApplication.portCardComponent "Uses"
        berrySend.singlePageApplication.portPage -> berrySend.singlePageApplication.portService "Uses"

        berrySend.singlePageApplication.profilePage -> berrySend.singlePageApplication.profileService "Uses"
        berrySend.singlePageApplication.profilePage -> berrySend.singlePageApplication.editProfileComponent "Sends to"

        berrySend.singlePageApplication.editProfileComponent -> berrySend.singlePageApplication.profileService "Uses"

        berrySend.singlePageApplication.authService -> berrySend.apiPlatform "[Requests authentication to use the application]"
        berrySend.singlePageApplication.userService -> berrySend.apiPlatform "[Requests user information]"
        berrySend.singlePageApplication.profileService -> berrySend.apiPlatform "[Requests user's profile information]"
        berrySend.singlePageApplication.portService -> berrySend.apiPlatform "[Requests information about ports and connections]"
        berrySend.singlePageApplication.optimizationService -> berrySend.apiPlatform "[Requests use of algorithms for optimization]"
        berrySend.singlePageApplication.graphService -> berrySend.apiPlatform "[Requests generation of graphs]"

        //
        // API Platform
        //
        berrySend.singlePageApplication -> berrySend.apiPlatform.routeOptimization "[Requests optimized routes]"
        berrySend.singlePageApplication -> berrySend.apiPlatform.portManagement "[Requests details of ports and its connections]"
        berrySend.singlePageApplication -> berrySend.apiPlatform.exportManagement "[Requests the planning and optimization of blue berries exports]"
        berrySend.singlePageApplication -> berrySend.apiPlatform.authentication "[Requests authentication to use the application]"
        berrySend.singlePageApplication -> berrySend.apiPlatform.profileManagement "[Requests creation and information about user profiles]"

        berrySend.apiPlatform.routeOptimization -> berrySend.apiPlatform.sharedKernel "Implements / extends base repository class"
        berrySend.apiPlatform.portManagement -> berrySend.apiPlatform.sharedKernel "Implements / extends base repository class"
        berrySend.apiPlatform.exportManagement -> berrySend.apiPlatform.sharedKernel "Implements / extends base repository class"
        berrySend.apiPlatform.authentication -> berrySend.apiPlatform.sharedKernel "Implements / extends base repository class"
        berrySend.apiPlatform.profileManagement -> berrySend.apiPlatform.sharedKernel "Implements / extends base repository class"

        berrySend.apiPlatform.routeOptimization -> berrySend.db "Reads from and writes to"
        berrySend.apiPlatform.portManagement -> berrySend.db "Reads from and writes to"
        berrySend.apiPlatform.exportManagement -> berrySend.db "Reads from and writes to"
        berrySend.apiPlatform.authentication -> berrySend.db "Reads from and writes to"
        berrySend.apiPlatform.profileManagement -> berrySend.db "Reads from and writes to"
        berrySend.apiPlatform.sharedKernel -> berrySend.db "Set ORM Mapping Rules, manages database context"

        berrySend.apiPlatform.routeOptimization -> berrySend.apiPlatform.authentication "Requests authentication for usage"
        berrySend.apiPlatform.portManagement -> berrySend.apiPlatform.authentication "Requests authentication for usage"
        berrySend.apiPlatform.exportManagement -> berrySend.apiPlatform.authentication "Requests authentication for usage"
        berrySend.apiPlatform.profileManagement -> berrySend.apiPlatform.authentication "Requests authentication for usage"

        berrySend.apiPlatform.routeOptimization -> berrySend.apiPlatform.portManagement "Obtains info about ports and connections for generating graphs for algorithms"
        berrySend.apiPlatform.exportManagement -> berrySend.apiPlatform.routeOptimization "Requests the generation of an optimized route for the requested export plan"
    }

    views {
        systemContext berrySend {
            include *
            autolayout lr
        }

        container berrySend {
            include *
            autolayout lr
        }

        component berrySend.singlePageApplication {
            include *
            autolayout lr
        }

        component berrySend.apiPlatform {
            include *
            autolayout lr
        }

        styles {
            element "ExternalSoftwareSystem" {
                stroke #979797
                color #979797
                shape box
            }
            element "App" {
                shape box
                stroke #EBA028
                color #EBA028
            }
            element "Web" {
                shape "WebBrowser"
                stroke #1B61E3
                color #1B61E3
            }
            element "API" {
                shape box
                stroke #342087
                color #342087
            }
            element "BD" {
                shape cylinder
                stroke #ec0e0e
                color #ec0e0e
            }
            element "Context" {
                shape "hexagon"
                stroke #dcb400
                color #dcb400
            }
            element "Element" {
                color #55aa55
                stroke #55aa55
                strokeWidth 7
                shape roundedbox
            }
            element "Person" {
                shape person
            }
            element "Boundary" {
                strokeWidth 1
            }
            relationship "Relationship" {
                thickness 4
            }
        }
    }

    configuration {
        scope softwaresystem
    }

}