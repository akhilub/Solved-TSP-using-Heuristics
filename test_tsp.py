import AKHILSIN_tsp as tsp
import veroviz as vrv
#import urllib3
#urllib3.disable_warnings()

ORS_API_KEY='5b3ce3597851110001cf62480fb8f5604a0b485b911812eedd4d31cf'

myBoundingRegion = [[43.01770145196991, -78.87840270996095], [42.878480017739044, -78.8756561279297], [42.83569550641454, -78.68270874023439], [42.96596996868038, -78.60717773437501], [43.04430359661548, -78.72528076171876]]

nodesDF = vrv.generateNodes(nodeType = 'customer',
                            nodeName = 'cust',
                            numNodes = 20,
                            incrementName = True,
                            nodeDistrib = 'uniformBB',
                            nodeDistribArgs = {'boundingRegion': myBoundingRegion},
                            snapToRoad = True,
                            dataProvider     = 'ORS-online',
                            dataProviderArgs = {'APIkey' : ORS_API_KEY})
#print(nodesDF)

[timeSec, distMeters] = vrv.getTimeDist2D(nodes = nodesDF,
                                          routeType = 'euclidean2D',
                                          speedMPS = vrv.convertSpeed(25, 'miles', 'hr', 'meters', 'second'))



response1 = tsp.solveTSP_SA(nodesDF,timeSec,2)
print(response1)