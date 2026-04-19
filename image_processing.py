import cv2
import numpy as np
import time

triangle_locations = []
circle_locations = []
hist_T = []
hist_C = []

def board_capture():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    result, image = cam.read()
    image = cv2.resize(image, (960,560))
    crop = image[10:500, 240:720]   
    cv2.imwrite('/home/pcblab/Downloads/FYP/alpha_image1.png',crop)
    return crop



def shape_detect(shape):
    board_capture()

    global j
    global triangle_locations, circle_locations, hist_T, hist_C

    
    xo_table = cv2.imread("/home/pcblab/Downloads/FYP/alpha_image1.png",cv2.IMREAD_GRAYSCALE)
   
    triangles = [cv2.imread("/home/pcblab/Downloads/FYP/alpha_triangle.png", cv2.IMREAD_GRAYSCALE),
                 cv2.imread("/home/pcblab/Downloads/FYP/alpha_triangle1.png", cv2.IMREAD_GRAYSCALE),
                 cv2.imread("/home/pcblab/Downloads/FYP/alpha_triangle2.png", cv2.IMREAD_GRAYSCALE),
                 cv2.imread("/home/pcblab/Downloads/FYP/alpha_triangle3.png", cv2.IMREAD_GRAYSCALE)]
                 #cv2.imread("/home/pcblab/Downloads/FYP/alpha_triangle4.png", cv2.IMREAD_GRAYSCALE)]
    
    o= cv2.imread("/home/pcblab/Downloads/FYP/alpha_circle.png",cv2.IMREAD_GRAYSCALE)
   
    
    # cv2.imshow('XO_table',xo_table)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    
    #cv2.imshow('triangle',)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    
    #cv2.imshow('circle',o)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
        
    font = cv2.FONT_HERSHEY_SIMPLEX 
    fontScale = 1
    color = (60, 255, 255)
    thickness = 2

    threshold = 0.76

    if shape == 'TRIANGLE':

        for triangle in triangles:
            result_x = cv2.matchTemplate(xo_table, triangle, cv2.TM_CCOEFF_NORMED)
            wx = triangle.shape[1]
            hx = triangle.shape[0]

            i = 1
            max_val = 1
            prev_min_val, prev_max_val, prev_min_loc, prev_max_loc = None, None, None, None
            while max_val > threshold:
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_x)
                    
                    if prev_min_val == min_val and prev_max_val == max_val and prev_min_loc == min_loc and prev_max_loc == max_loc:
                        break
                    else:
                            prev_min_val, prev_max_val, prev_min_loc, prev_max_loc = min_val, max_val, min_loc, max_loc
                        
                    if max_val > threshold:
                            start_row = max(0, max_loc[1] - hx // 2)
                            start_col = max(0, max_loc[0] - wx // 2)
                            end_row = min(result_x.shape[0], max_loc[1] + hx // 2 + 1)
                            end_col = min(result_x.shape[1], max_loc[0] + wx // 2 + 1)
                            

                            result_x[start_row: end_row, start_col: end_col] = 0
                            xo_table = cv2.rectangle(xo_table,(max_loc[0],max_loc[1]), (max_loc[0]+wx+1, max_loc[1]+hx+1), (0,255,0) )
                            xo_table = cv2.putText(xo_table, 'Triangle' + str(i), max_loc, font, fontScale, color, thickness, cv2.LINE_AA) 
                            mid_pt = (max_loc[0] + wx // 2, max_loc[1] + hx // 2)
                            if (mid_pt[0] > 329 and mid_pt[0] < 454) and (mid_pt[1] > 355 and mid_pt[1] < 475):
                                if 1 not in triangle_locations:
                                    if 1 not in hist_T: 
                                        triangle_locations.append(1)
                                        hist_T.append(1)
                                else:
                                    triangle_locations.remove(1)
                            elif (mid_pt[0] > 175 and mid_pt[0] < 305) and (mid_pt[1] > 355 and mid_pt[1] < 475):
                                if 2 not in triangle_locations:
                                    if 2 not in hist_T: 
                                        triangle_locations.append(2)
                                        hist_T.append(2)
                                else:
                                    triangle_locations.remove(2)
                            elif (mid_pt[0] > 29 and mid_pt[0] < 151) and (mid_pt[1] > 355 and mid_pt[1] < 475):
                                if 3 not in triangle_locations:
                                    if 3 not in hist_T: 
                                        triangle_locations.append(3)
                                        hist_T.append(3)
                                else:
                                    triangle_locations.remove(3)
                            elif (mid_pt[0] > 329 and mid_pt[0] < 454) and (mid_pt[1] > 200 and mid_pt[1] < 312):
                                if 4 not in triangle_locations:
                                    if 4 not in hist_T: 
                                        triangle_locations.append(4)
                                        hist_T.append(4)
                                else:
                                    triangle_locations.remove(4)
                            elif (mid_pt[0] > 175 and mid_pt[0] < 305) and (mid_pt[1] > 200 and mid_pt[1] < 312):
                                if 5 not in triangle_locations:
                                    if 5 not in hist_T: 
                                        triangle_locations.append(5)
                                        hist_T.append(5)
                                else:
                                    triangle_locations.remove(5)
                            elif (mid_pt[0] > 29 and mid_pt[0] < 151) and (mid_pt[1] > 200 and mid_pt[1] < 312):
                                if 6 not in triangle_locations:
                                    if 6 not in hist_T: 
                                        triangle_locations.append(6)
                                        hist_T.append(6)
                                else:
                                    triangle_locations.remove(6)
                            elif (mid_pt[0] > 329 and mid_pt[0] < 454) and (mid_pt[1] > 43 and mid_pt[1] < 153):
                                if 7 not in triangle_locations:
                                    if 7 not in hist_T: 
                                        triangle_locations.append(7)
                                        hist_T.append(7)
                                else:
                                    triangle_locations.remove(7)
                            elif (mid_pt[0] > 175 and mid_pt[0] < 305) and (mid_pt[1] > 43 and mid_pt[1] < 153):
                                if 8 not in triangle_locations:
                                    if 8 not in hist_T: 
                                        triangle_locations.append(8)
                                        hist_T.append(8)
                                else:
                                    triangle_locations.remove(8)
                            elif (mid_pt[0] > 29 and mid_pt[0] < 151) and (mid_pt[1] > 43 and mid_pt[1] < 153):
                                if 9 not in triangle_locations:
                                    if 9 not in hist_T:
                                        triangle_locations.append(9)
                                        hist_T.append(9)
                                else:
                                    triangle_locations.remove(9)
                            
                            i += 1

        return triangle_locations[0]



    elif shape == "CIRCLE":

        result_o = cv2.matchTemplate(xo_table, o, cv2.TM_CCOEFF_NORMED)

        wo = o.shape[1]
        ho = o.shape[0]

        threshold_o = 0.76
    
        i = 1
        max_val = 1
        prev_min_val, prev_max_val, prev_min_loc, prev_max_loc = None, None, None, None
        while max_val > threshold_o:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_o)
            
            if prev_min_val == min_val and prev_max_val == max_val and prev_min_loc == min_loc and prev_max_loc == max_loc:
                break
            else:
                prev_min_val, prev_max_val, prev_min_loc, prev_max_loc = min_val, max_val, min_loc, max_loc
                
            if max_val > threshold_o:
                    start_row = max(0, max_loc[1] - ho // 2)
                    start_col = max(0, max_loc[0] - wo // 2)
                    end_row = min(result_o.shape[0], max_loc[1] + ho // 2 + 1)
                    end_col = min(result_o.shape[1], max_loc[0] + wo // 2 + 1)

                    result_o[start_row: end_row, start_col: end_col] = 0
                    xo_table = cv2.rectangle(xo_table,(max_loc[0],max_loc[1]), (max_loc[0]+wo+1, max_loc[1]+ho+1), (0,255,0) )
                    xo_table = cv2.putText(xo_table, 'Circle' + str(i), max_loc, font, fontScale, color, thickness, cv2.LINE_AA) 

                    mid_pt = (max_loc[0] + wo // 2, max_loc[1] + ho // 2)
                    if (mid_pt[0] > 329 and mid_pt[0] < 454) and (mid_pt[1] > 355 and mid_pt[1] < 475):
                        if 1 not in circle_locations:
                            if 1 not in hist_C: 
                                circle_locations.append(1)
                                hist_C.append(1)
                        else:
                            circle_locations.remove(1)
                    elif (mid_pt[0] > 175 and mid_pt[0] < 305) and (mid_pt[1] > 355 and mid_pt[1] < 475):
                        if 2 not in circle_locations:
                            if 2 not in hist_C: 
                                circle_locations.append(2)
                                hist_C.append(2)
                        else:
                            circle_locations.remove(2)
                    elif (mid_pt[0] > 29 and mid_pt[0] < 151) and (mid_pt[1] > 355 and mid_pt[1] < 475):
                        if 3 not in circle_locations:
                            if 3 not in hist_C: 
                                circle_locations.append(3)
                                hist_C.append(3)
                        else:
                            circle_locations.remove(3)
                    elif (mid_pt[0] > 329 and mid_pt[0] < 454) and (mid_pt[1] > 200 and mid_pt[1] < 312):
                        if 4 not in circle_locations:
                            if 4 not in hist_C: 
                                circle_locations.append(4)
                                hist_C.append(4)
                        else:
                            circle_locations.remove(4)
                    elif (mid_pt[0] > 175 and mid_pt[0] < 305) and (mid_pt[1] > 200 and mid_pt[1] < 312):
                        if 5 not in circle_locations:
                            if 5 not in hist_C: 
                                circle_locations.append(5)
                                hist_C.append(5)
                        else:
                            circle_locations.remove(5)
                    elif (mid_pt[0] > 29 and mid_pt[0] < 151) and (mid_pt[1] > 200 and mid_pt[1] < 312):
                        if 6 not in circle_locations:
                            if 6 not in hist_C: 
                                circle_locations.append(6)
                                hist_C.append(6)
                        else:
                            circle_locations.remove(6)
                    elif (mid_pt[0] > 329 and mid_pt[0] < 454) and (mid_pt[1] > 43 and mid_pt[1] < 153):
                        if 7 not in circle_locations:
                            if 7 not in hist_C: 
                                circle_locations.append(7)
                                hist_C.append(7)
                        else:
                            circle_locations.remove(7)
                    elif (mid_pt[0] > 175 and mid_pt[0] < 305) and (mid_pt[1] > 43 and mid_pt[1] < 153):
                        if 8 not in circle_locations:
                            if 8 not in hist_C: 
                                circle_locations.append(8)
                                hist_C.append(8)
                        else:
                            circle_locations.remove(8)
                    elif (mid_pt[0] > 29 and mid_pt[0] < 151) and (mid_pt[1] > 43 and mid_pt[1] < 153):
                        if 9 not in circle_locations:
                            if 9 not in hist_C:
                                circle_locations.append(9)
                                hist_C.append(9)
                        else:
                            circle_locations.remove(9)

                    i += 1
        return circle_locations[0]   
    
    print("Triangle Locations:", triangle_locations)
    print("Circle Locations:", circle_locations)


# def main():

#     while True:
#        str=input("Do you want to click a picture(y/n)?")
#        if str=='y':
#          shape_detect()
#        elif str=='n':
#           exit()


# if __name__ == "__main__":
#     main()
