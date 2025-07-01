from rest_framework import serializers
from .models import FoodItem, CompanyFoodItem, FoodCategory

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
    category = FoodCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=FoodCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'image', 'category', 'category_id', 'group', 'food_type']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)

class CompanyFoodItemSerializer(serializers.ModelSerializer):
    food_item_detail = FoodItemSerializer(source='food_item', read_only=True)

    class Meta:
        model = CompanyFoodItem
        fields = ['id', 'company', 'food_item', 'food_item_detail', 'price', 'is_available', 'special_tag', 'special_note']
