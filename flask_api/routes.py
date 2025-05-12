from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from movie_review.reviews.models import Review
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add custom fields if needed
    pass

User = get_user_model()  

class Review(models.Model):
    movie_title = models.CharField(max_length=255)
    rating = models.IntegerField()
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Authentication parser
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', type=str, required=True, help='Username is required')
auth_parser.add_argument('password', type=str, required=True, help='Password is required')

# Review parser
review_parser = reqparse.RequestParser()
review_parser.add_argument('movie_title', type=str, required=True, help='Movie title is required')
review_parser.add_argument('rating', type=int, required=True, help='Rating is required')
review_parser.add_argument('content', type=str, required=True, help='Content is required')

class AuthResource(Resource):
    def post(self):
        args = auth_parser.parse_args()
        user = authenticate(username=args['username'], password=args['password'])
        
        if user:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class RegisterResource(Resource):
    def post(self):
        args = auth_parser.parse_args()
        
        if User.objects.filter(username=args['username']).exists():
            return {'message': 'Username already exists'}, 400
            
        user = User.objects.create_user(
            username=args['username'],
            password=args['password']
        )
        
        access_token = create_access_token(identity=user.id)
        return {
            'message': 'User created successfully',
            'access_token': access_token
        }, 201

class ReviewResource(Resource):
    @jwt_required()
    def get(self, review_id=None):
        if review_id:
            try:
                review = Review.objects.get(id=review_id)
                return {
                    'id': review.id,
                    'movie_title': review.movie_title,
                    'rating': review.rating,
                    'content': review.content,
                    'user': review.user.username,
                    'created_at': review.created_at.isoformat()
                }
            except ObjectDoesNotExist:
                return {'message': 'Review not found'}, 404
        else:
            reviews = Review.objects.all()
            return [{
                'id': review.id,
                'movie_title': review.movie_title,
                'rating': review.rating,
                'content': review.content,
                'user': review.user.username,
                'created_at': review.created_at.isoformat()
            } for review in reviews]

    @jwt_required()
    def post(self):
        args = review_parser.parse_args()
        current_user_id = get_jwt_identity()
        
        try:
            user = User.objects.get(id=current_user_id)
            review = Review.objects.create(
                movie_title=args['movie_title'],
                rating=args['rating'],
                content=args['content'],
                user=user
            )
            return {
                'id': review.id,
                'movie_title': review.movie_title,
                'rating': review.rating,
                'content': review.content,
                'user': review.user.username,
                'created_at': review.created_at.isoformat()
            }, 201
        except Exception as e:
            return {'message': str(e)}, 400

    @jwt_required()
    def put(self, review_id):
        args = review_parser.parse_args()
        current_user_id = get_jwt_identity()
        
        try:
            review = Review.objects.get(id=review_id)
            if review.user.id != current_user_id:
                return {'message': 'Not authorized to edit this review'}, 403
                
            review.movie_title = args['movie_title']
            review.rating = args['rating']
            review.content = args['content']
            review.save()
            
            return {
                'id': review.id,
                'movie_title': review.movie_title,
                'rating': review.rating,
                'content': review.content,
                'user': review.user.username,
                'created_at': review.created_at.isoformat()
            }
        except ObjectDoesNotExist:
            return {'message': 'Review not found'}, 404

    @jwt_required()
    def delete(self, review_id):
        current_user_id = get_jwt_identity()
        
        try:
            review = Review.objects.get(id=review_id)
            if review.user.id != current_user_id:
                return {'message': 'Not authorized to delete this review'}, 403
                
            review.delete()
            return {'message': 'Review deleted successfully'}, 200
        except ObjectDoesNotExist:
            return {'message': 'Review not found'}, 404

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reviews',  # Add this if not already present
    'users',    # Add this if not already present
]