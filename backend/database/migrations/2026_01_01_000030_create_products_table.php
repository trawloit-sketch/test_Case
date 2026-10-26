<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     * Tabel products — katalog produk garam
     */
    public function up(): void
    {
        Schema::create('products', function (Blueprint $table) {
            $table->id();
            $table->string('product_code', 20)->unique()->comment('Kode unik produk, contoh: GRM-KNS-001');
            $table->string('product_name', 200)->comment('Nama lengkap produk');
            $table->foreignId('category_id')
                  ->nullable()
                  ->constrained('product_categories')
                  ->nullOnDelete()
                  ->comment('Relasi ke tabel product_categories');
            $table->string('unit', 30)->comment('Satuan produk: Bungkus, Karung, Pack, Bata, dll');
            $table->decimal('unit_price', 15, 2)->default(0)->comment('Harga jual per satuan dalam rupiah');
            $table->integer('minimum_stock')->default(0)->comment('Batas minimum stok sebelum reorder');
            $table->boolean('is_active')->default(true)->comment('Status aktif produk');
            $table->text('description')->nullable()->comment('Deskripsi produk (opsional)');
            $table->timestamps();
            $table->softDeletes();

            // Index untuk pencarian dan filter
            $table->index('category_id');
            $table->index('is_active');
            $table->index('product_name');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('products');
    }
};
