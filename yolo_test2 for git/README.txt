Deep learning tutorial.(requirement: understand deep learning first, this tutorial won't teach you the basic. XD)

1. installation of tensorflow
	a)Before you start, please make sure you create an environment. Anaconda is a good environment tool. Environment will save your life if you screwed up by installing things that not compatible with the 		tensorflow. When you screwed up, all you need to do is just re-create the environment :)  
	Download link: https://www.anaconda.com/distribution/

	b)After that, you can start installing tensorflow. From my experience, there’s 1000 ways you could go wrong installing tensorflow, that’s why you need environment. Incompatible cuda,cudnn or bla bla 		bla. And the solution to this is let conda to help you install whatever you need.
	*you can replace tf_gpu with the name of the environment you want*
	Command line :    conda create --name tf_gpu tensorflow-gpu

2. download the file from   https://drive.google.com/file/d/1_GhHrs792hcEYrhwA3MszNy_tBR1gYrr/view?usp=sharing
   Before continue, install (keras >= 2.0.8 and imgaug)
   We get out deep learning code from https://github.com/experiencor/keras-yolo2, but we did some modification
   Currently, we are using tiny-yolo as feature extractor. 
    a)Frontend.py: line 61 and line 72 is to joined the feature extractor and the detection layer 
                 : To do transfer learning ,uncomment 75,76 to do freeze the feature extractor
                 : line 374 I made it to saved the model when the training stop(it run till the end or early stopage)
    b)Backend.py : Commented out loading weight, as we want to train the feature extractor layers and detection layer as a whole model.
                 : For tiny Yolo, we added dropout to every conv layer,dropout rate can be change at line 11
    c)preprocessing.py : We disable the online geometric augmentation here, because we want to make offline geo aug. line 66 is set to false. Offline aug with imgaug give more freedom.
    d)utils.py : line 46, by setting config.gpu_options.per_process_gpu_memory_fraction = 0.5 , we restricting the gpu to use more than 50 % .basically restrict it a bit to allow other code to            				 run(etc:barrier tape detection)
               : In xavier:
    e)predict.py: added prediction using webcam. 
    
   
Currently, our best model is ourbestbestmodel.h5. You can do transfer learning using this model.

3. Data preparation
   a)After data collection, you can upload the pictures to label box, that's a cloud that enable a lot of ppl to help with labeling.
   b)After finish labeling, you can download the data as pascal voc.
   c)Usually there's issue with the xml files, some labels will be in polygon shape instead of rectangle shape. So you have to remove the polygon shape.
        To check whether there's polygon in the xml , grep -r "polygon" in the data folder.
        To do that:   grep -r -il "polygon" ./all_labels/* | xargs -n1 -ti mv {} ./wrong_label
        All the xml files with "polygon " will be moved to wrong_label
   d)Now you have to remove the polygon from the xml files.
        To do that: edit the file path in delete_polygon.py, and execute it.
   e)then you have to move out the image of the wrong_label from all images.
        To do that: edit the file path in moving.py and execute it.
   f) check the missing label by using labelImg https://github.com/tzutalin/labelImg, and label it.
   
# you will be doing a lot of shifting files,example:  mv /home/nvidia/keras-yolo2/export/*.xml /home/nvidia/keras-yolo2/train_labels
### Since we have a good base model, actually we can let the model to predict the photos and generate xml file ,so we only need to correct the wrong label and feed to the network to train again.(Still in progress )  ###
 
4. Data Augmentation
   a)For geometric augmentation, go to data_augmentation folder , edit the the 3 path in  image_imgaug.py and excute it.(of course you can edit the parameters of the augmentation before excecuting it) 
   b)colour brightness thoes are online augmentation when doing training.
   

5. Training  (learn transfer learning before you come here)
   a) Change the config.json 
   
{
    "model" : {
        "backend":              "Tiny Yolo",      # the feature extractor we using now 
        "input_size":           416,              #input size of images    
        "anchors":              [1.39,1.30, 1.75,3.36, 3.42,1.88, 3.83,0.88, 4.26,4.03],   # this one you can generate using gen_anchors.py
         "max_box_per_image":    10,        
        "labels":               ["F20_20_B", "F20_20_G", "S40_40_B", "S40_40_G", "M20_100", "M20", "M30", "R20", "Bearing_Box", "Bearing", "Axis","Distance_Tube","Motor"]
    },

    "train": {
        "train_image_folder":   "/home/ariccspstk/keras-yolo2/standing_image/",       # the images file
        "train_annot_folder":   "/home/ariccspstk/keras-yolo2/standing_label/",       # the label file
        "NOTE:choices_of_mode":  "train or eval,both",                          
        "mode":                 "both",                                               #just kept it as both, it will train and evaluate your model
        "train_times":         2	,                                                 # if your data is big enough, can set it as 1, if not can increase it 
        "pretrained_weights":   "ourbestbestmodel.h5",                                #get the weight from this model, if you leave it empty, it will train from scratch, but we can do transfer learning 
        "batch_size":           64,                                                   # for our gpu, 64 is the max we can use.
        "learning_rate":        1e-4,                                                 # this one hmmm, you go learn before you touch this.
        "nb_epochs":            100,                                                  # just leave it as 100, it will stop when there's no improvement
        "warmup_epochs":        3,


          #### this is the punishment part , this one need to change according to how your model performing###
        "object_scale":         5.0 ,           # determine how much to penalize wrong prediction of confidence of object predictors
        "no_object_scale":      3.0,            # determine how much to penalize wrong prediction of confidence of non-object predictors
        "coord_scale":          1.0,            # determine how much to penalize wrong position and size predictions (x, y, w, h)
        "class_scale":          5.0,            # determine how much to penalize wrong class prediction

        "saved_weights_name":   "new_model.h5",    ## it will saved as this file,when there's improvement. but when the training stop,it will save the model as final_weight.h5. usually , I will use the final_weight.h5, but you can compare between this and the new_model.h5. 
        "debug":                false
    },

    "valid": { 
        "valid_image_folder":   "",         ## this one just leave it empty, our code will split 80/20% from the train image
        "valid_annot_folder":   "",

        "valid_times":          1
    }
}

   b)to start training:  python train.py -c config.json
   
6. test your model with webcam.
   python predict.py -c config.json -w (name of your weight)  -i (usually is 0 or 1(the webcam no.))
   
   
