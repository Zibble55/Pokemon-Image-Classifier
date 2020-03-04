# This project will focus on image classification. Specifically, we will be starting with an image set of 
# Pokemon from the first 7 generations of the game. The goal is to classify each image as a type of Pokemon.

# We start with the website https://shirinsplayground.netlify.com/2018/06/keras_fruits/ for instruction.

setwd("/Users/denni/Documents/pokemon-images-and-types")

type<-read.csv("pokemon.csv")

# First, we will only consider the first type. Plan to redo with the types combinded in some way in the future.

type1<-type[-3]

types<-as.character(unique(type1$Type1))

numtypes<-length(types)

# Not sure yet what this library does. Just going along with it.

library(keras)

# Uncomment when starting a new R session
#install_keras()

# Changing the image's scale

img_width<-20
img_height<-20

target_size<-c(img_width,img_height)

channels<-3

# Path to image folders seperated into type folders. Refer to python code to randomly arrange img files.

train_image_files_path<-"/Users/denni/Documents/pokemon-images-and-types/images/train/train"
test_image_files_path<-"/Users/denni/Documents/pokemon-images-and-types/images/test/test"


# optional data augmentation
train_data_gen = image_data_generator(
  rescale = 1/255 #,
  #rotation_range = 40,
  #width_shift_range = 0.2,
  #height_shift_range = 0.2,
  #shear_range = 0.2,
  #zoom_range = 0.2,
  #horizontal_flip = TRUE,
  #fill_mode = "nearest"
)

# Test data shouldn't be augmented! But it should also be scaled.
test_data_gen <- image_data_generator(rescale = 1/255)  

# training images
train_image_array_gen <- flow_images_from_directory(train_image_files_path, train_data_gen,
                                                    target_size = target_size,
                                                    class_mode = "categorical",
                                                    classes = types,
                                                    seed = 42)

# test images
test_image_array_gen <- flow_images_from_directory(test_image_files_path, 
                                                    test_data_gen,
                                                    target_size = target_size,
                                                    class_mode = "categorical",
                                                    classes = types,
                                                    seed = 42)


cat("Number of images per class:")

table(factor(train_image_array_gen$classes))

train_image_array_gen$class_indices

types_indices <- train_image_array_gen$class_indices
save(types_indices, file = "/Users/denni/Documents/types_indices.RData")

# number of training samples
train_samples <- train_image_array_gen$n
# number of validation samples
test_samples <- test_image_array_gen$n

# define batch size and number of epochs
batch_size <- 32
#epochs<- 10
epochs <- 30



# Neural Network Model

# Need to read more into this. Don't understand it well enough to edit yet.

# initialise model
model <- keras_model_sequential()

# add layers
model %>%
  layer_conv_2d(filter = 32, kernel_size = c(3,3), padding = "same", input_shape = c(img_width, img_height, channels)) %>%
  layer_activation("relu") %>%
  
  # Second hidden layer
  layer_conv_2d(filter = 16, kernel_size = c(3,3), padding = "same") %>%
  layer_activation_leaky_relu(0.5) %>%
  layer_batch_normalization() %>%
  
  # Use max pooling
  layer_max_pooling_2d(pool_size = c(2,2)) %>%
  layer_dropout(0.25) %>%
  
  # Flatten max filtered output into feature vector 
  # and feed into dense layer
  layer_flatten() %>%
  layer_dense(100) %>%
  layer_activation("relu") %>%
  layer_dropout(0.5) %>%
  
  # Outputs from dense layer are projected onto output layer
  layer_dense(as.numeric(numtypes)) %>% 
  layer_activation("softmax")

# compile
model %>% compile(
  loss = "categorical_crossentropy",
  optimizer = optimizer_rmsprop(lr = 0.0001, decay = 1e-6),
  metrics = "accuracy"
)

# fit
# Something is wrong with this fit. Cretes an error "ImportError: Could not import PIL.IMage. The use of 'load_img' 
# requires PIL." unless install_tensorflow() is reinstalled. Reinstalling changes _gen data to ones with null pointers
# and causes the error " 'what' must be a function or character string". Need to look into this

# Update: running install_tensorflow() fixes the issue


hist <- model %>% fit_generator(
  # training data
  train_image_array_gen,
  
  # epochs
  steps_per_epoch = as.integer(train_samples / batch_size), 
  epochs = epochs, 
  
  # test data
  validation_data = test_image_array_gen,
  validation_steps = as.integer(test_samples / batch_size),
  
  # print progress
  verbose = 2,
  callbacks = list(
    # save best model after every epoch
    callback_model_checkpoint("/Users/denni/Documents/pokemon-images-and-types/pokemon_checkpoints.h5", save_best_only = TRUE),
    # only needed for visualising with TensorBoard
    callback_tensorboard(log_dir = "/Users/denni/Documents/pokemon-images-and-types/logs")
  )
)

install_tensorflow()
plot(hist)


require(EBImage)

# Results: epoch at 10 gave us about 17.1% accuracy and 17.7% val_accuracy.
#          epoch at 20 gives slightly higher with 26.3% accuracy and 18.11 val.accuracy
#          best at epoch at 17 with 22% accuracy and 21.4% val_accuracy
#          Batch was at 15 for all of these

# Trying different neural network models

# Changed batch to 32 and results went down. Training set is at size 566.
# Results: epoch at 30 has 24.5% accuracy and 21.9% val_accuracy
