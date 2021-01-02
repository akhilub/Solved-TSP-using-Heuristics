def solveTSP_SA(nodesDF, costDict, timeLimit):
    import time
    from random import random
    import math as m
    import veroviz as vrv
    #import urllib3
    #urllib3.disable_warnings()
    
    ORS_API_KEY='5b3ce3597851110001cf62480fb8f5604a0b485b911812eedd4d31cf'
    
    
    def solve_tsp_nn(startNode, costDict, nodesDF): 
        """
        This function computes a "nearest neighbor" solution to a TSP.
        
        Inputs
        ------
        startNode: Integer, indicating the node where the salesperson begins (and ends) the route
        
        costDict: VeRoViz time or distance dictionary.
        
        nodesDF: VeRoViz nodes dataframe
        
        Returns
        -------
        An ordered list of nodeIDs specifying a TSP route.
        """
        
        # Solve the TSP with a "nearest neighbor" heuristic
        nn_route = []
    
        # Start our route by visiting the startNode
        nn_route.append(startNode)
    
        # Initialize a list of unvisited nodes
        unvisitedNodes = list(nodesDF[nodesDF['id'] != startNode]['id'])
    
        # Let i represent our "current" location:
        i = startNode
    
        while len(unvisitedNodes) > 0:
            # Initialize minTime to a huge value
            minTime = float('inf')
    
            # Find the nearest unvisited node to our current node:
            for j in unvisitedNodes:
                if (costDict[i,j] < minTime):
                    nextNode = j
                    minTime = costDict[i,j]
    
            # Update our salesperson's location
            i = nextNode
    
            # Append nextNode to our route:
            nn_route.append(nextNode)
    
            # Remove nextNode from our list of unvisitedNodes:
            unvisitedNodes.remove(nextNode)
    
        nn_route.append(startNode)
    
        return nn_route    
    
    def tsp_cost(route, costDict):
        cost = 0
        
        i = route[0]
        for j in route[1:]:
            cost += costDict[i,j]
            i = j
            
        cost += costDict[i, route[0]]
        
        return cost
    
    def tsp_neighbor(route):
        """
        This function computes a "subtour" solution to a TSP.
        
        Inputs
        ------
        route: list of Integer, indicating the node where the salesperson begins (and ends) the route
        
        Returns
        -------
        A random list of nodeIDs specifying another TSP route.
        """
        #import random
        from random import randint 
        
        #a = random.randint(0,len(route)-3)
        a = randint(0,len(route)-3)
        #b = random.randint(a+1, len(route)-2)
        b = randint(a+1, len(route)-2)
        
        newRoute = []
        newRoute.extend(route[0:a])
        
        subtour = route[a:b+1]
        subtour.reverse()
        newRoute.extend(subtour)
        
        newRoute.extend(route[b+1:len(route)-1])
        
        newRoute.append(newRoute[0])
        
        return newRoute
    
    
    print(nodesDF)
    
    # Simulated annealing (SA) procedure--Phase I
    # Initialize parameters 
    runTime=0
    start_time = time.time()
    startnode=1   #"home location"
    T0=4000
    I=10
    d=5
    Tfinal=2020
    cutoffTime=timeLimit
    
    # Initial solution by calling nearest neighbor function
    X0 = solve_tsp_nn(startnode,costDict,nodesDF)
    Z=tsp_cost(X0,costDict)
    print('Intial Solution : X0 =',X0,'Z0 =',Z)
    
    # Find current solution by calling neighbor/subtour function
    Xcur = tsp_neighbor(X0)
    Zcur = tsp_cost(Xcur,costDict)    
    Tcur = T0
    print('Current Solution : Xcur =',Xcur,'Zcur =',Zcur)
    Xbest = Xcur
    Zbest = Zcur
    print('Best known Solution : Xbest =',Xbest,'Zbest =',Zbest)
    
    #Simulated Annealing Procedure - Phase II
    def solveTSP_SA2(I,X0,Z,Xcur,Zcur,Xbest,Zbest,Tcur,d,Tfinal,runTime):
        #print('Tcur=',Tcur)
        for i in range(1,I+1):
            #Generate a neighbor solution, Xcount
            #call tsp_neighbor(route)
            Xcount=tsp_neighbor(X0)
            Z = tsp_cost(Xcount,costDict)
            #print('i=',i)
            #print('Xcount=',Xcount,'Zcount=',Z)

            if (Z<Zcur):
                #print('Z-Zcur=',Z-Zcur)
                Xcur = Xcount
                Zcur = Z
                #print('Xcur=',Xcur,'Zcur=',Z)


            else:
                C=Z-Zcur
                #print('C=',C)
                if(random()<=m.exp(-C/Tcur)):
                    Xcur = Xcount
                    Zcur = Z
                    #print('Xcur=',Xcur,'Zcur=',Zcur)


            if(Z < Zbest):
                #print('Z-Zbest=',Z-Zbest)
                Zbest = Z
                Xbest = Xcur
                #print('Xbest=',Xbest,'Zbest=',Zbest)

        Tcur=Tcur-d
        #print('Tcur=',Tcur)
        #print('Xbest=',Xbest,'Zbest=',Zbest)
            
        runTime=time.time()-start_time
        #print(runTime)
        
        #Simulated Annealing Procedure - Phase III
        if(Tcur<Tfinal or runTime>=timeLimit):
            if(Tcur<Tfinal):
                print('Tcur=',Tcur,'< Tfinal=',Tfinal)
                print('runTime =',runTime,',cutoffTime =',cutoffTime)
            elif(runTime>=cutoffTime):
                print('runTime =',runTime,'> cutoffTime =',cutoffTime)
                print('Tcur=',Tcur,',Tfinal=',Tfinal)
            return Xbest,Zbest

        return solveTSP_SA2(I,X0,Z,Xcur,Zcur,Xbest,Zbest,Tcur,d,Tfinal,runTime)
    
    
    
    XBEST,ZBEST=solveTSP_SA2(I,X0,Z,Xcur,Zcur,Xbest,Zbest,Tcur,d,Tfinal,runTime)
    print('Best Solution from SA : XBEST=',XBEST,'ZBEST=',ZBEST)
    
    totalruntime=time.time()-start_time
    print('totaltime=',totalruntime)
    
    # SA produces a "best" solution, XBEST.
    # XBEST is just a sequence of node numbers,
    # starting from and returning to a "home" location.
    # For example, Xbest = [1, 5, 3, 4, 2, 1].
    
    # Your function should return a VeRoViz "assignments" dataframe.
    # Fortunately, VeRoViz provides a function to make this very easy:
    assignmentsDF = vrv.createAssignmentsFromNodeSeq2D(
        nodeSeq          = XBEST,
        nodes            = nodesDF,
        objectID         = 'Blue Car',
        modelFile        = 'veroviz/models/car_blue.gltf',
        modelScale       = 100,
        modelMinPxSize   = 75,
        routeType        = 'fastest',
        speedMPS         = None,
        leafletColor     = 'blue',
        leafletWeight    = 3,
        leafletStyle     = 'dashed',
        leafletOpacity   = 0.8,
        useArrows        = True,
        cesiumColor      = 'blue',
        cesiumWeight     = 3,
        cesiumStyle      = 'solid',
        cesiumOpacity    = 0.8,
        dataProvider     = 'ORS-online',
        dataProviderArgs = {'APIkey' : ORS_API_KEY})

    # See https://veroviz.org/docs/veroviz.createAssignments.html#veroviz.createAssignments.createAssignmentsFromNodeSeq2D
    # for more info on this function.
    
    return assignmentsDF

